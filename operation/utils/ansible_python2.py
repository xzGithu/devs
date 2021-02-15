# coding:utf-8

"""
通过API动态生成ansible资产信息，用于集群组建的部署，软件的安装,
"""

import sys
import json
import shutil  # 用于读取YAML和JSON格式的文件
from ansible.parsing.dataloader import DataLoader  # 用于存储各类变量信息
from ansible.vars.manager import VariableManager
from ansible import constants as C  # 用于获取ansible内置的一些常量
from ansible.module_utils.common.collections import ImmutableDict  # 用于自定制一些选项
from ansible import context  # 上下文管理器，他就是用来接收 ImmutableDict 的示例对象
from ansible.inventory.manager import InventoryManager  # 管理资产文件（动态资产、静态资产）或者主机列表
from ansible.playbook.play import Play  # 用于执行 Ad-hoc 的核心类，即ansible相关模块，命令行的ansible -m方式
from ansible.executor.task_queue_manager import TaskQueueManager  # ansible 底层用到的任务队列管理器
from ansible.executor.playbook_executor import PlaybookExecutor  # 执行 playbook 的核心类，即命令行的ansible-playbook *.yml
from ansible.errors import AnsibleError  # ansible 自身的一些异常
from ansible.plugins.callback import CallbackBase  # 回调基类，处理ansible的成功失败信息，这部分对于二次开发自定义可以做比较多的自定义


class PlaybookCallbackModule(CallbackBase):
    """
    重写playbook callbackBase类
    """

    def __init__(self, *args, **kwargs):
        super(PlaybookCallbackModule, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_skipped = {}
        self.host_unreachable = {}
        self.host_failed = {}
        self.host_status = {}
        self.host_password = None

    def v2_runner_on_unreachable(self, result):
        if result._host.get_name() in self.host_unreachable.keys():
            self.host_unreachable[result._host.get_name()].append(result.task_name)
        else:
            self.host_unreachable[result._host.get_name()] = [result.task_name]

    def v2_runner_on_ok(self, result, *args, **kwargs):
        print(result, 'resulennnnnnnnnnnnnnnnn')
        if result._host.get_name() in self.host_ok.keys():
            try:
                # self.host_ok[result._host.get_name()].append(result.task_name+':'+result._result["stderr"])
                self.host_ok[result._host.get_name()].append(result.task_name + result._result["stderr"])
            except:
                self.host_ok[result._host.get_name()].append(result.task_name)
        else:
            try:
                self.host_ok[result._host.get_name()] = [result.task_name + result._result["stderr"]]
                # self.host_ok[result._host.get_name()] = [result.task_name+':'+result._result["stderr"]]
            except:
                self.host_ok[result._host.get_name()] = [result.task_name]
        if result.task_name == 'get elastic password':
            self.host_password = result._result["stdout"]
        # print(result._result)
        print(self.host_ok)
        # self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        if result._host.get_name() in self.host_failed.keys():
            self.host_failed[result._host.get_name()].append(result.task_name + ':' + result._result["msg"])
        else:
            self.host_failed[result._host.get_name()] = [result.task_name + ':' + result._result["msg"]]
            # print(result._result)
            # self.host_failed[result._host.get_name()] = result

    def v2_runner_on_skipped(self, result):
        if result._host.get_name() in self.host_skipped.keys():
            self.host_skipped[result._host.get_name()].append(result.task_name)
        else:
            self.host_skipped[result._host.get_name()] = [result.task_name]
            # self.host_skipped[result._host.get_name()] = result

    def v2_playbook_on_stats(self, stats):
        hosts = sorted(stats.processed.keys())
        for h in hosts:
            t = stats.summarize(h)
            self.host_status[h] = {
                "ok": t['ok'],
                "changed": t['changed'],
                "unreachable": t['unreachable'],
                "skipped": t['skipped'],
                "failed": t['failures']
            }


class ResuCallbackModule(CallbackBase):
    """
    重写command callbackBase类
    """

    def __init__(self, *args, **kwargs):
        super(ResuCallbackModule, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result


class MyInventory:
    def __init__(self, hostsresource, sources=None):
        """
        初始化函数
        :param hostsresource: 主机资源可以有2种形式
        列表形式: [{"ip": "192.168.1.1", "port": "22", "username": "root", "password": "123456"}]
        字典形式: {
                    "Group1": {
                        "hosts": [{"ip": "192.168.1.1", "port": "22", "username": "root", "password": None}],
                        "vars": {"var": "ansible"}
                }
        """
        self._hostsresource = eval(hostsresource)
        print(self._hostsresource)
        print(type(self._hostsresource))
        self._loader = DataLoader()
        self._hostsfilelist = ["hosts"]
        self._inventory = InventoryManager(loader=self._loader, sources=sources)
        self._variable_manager = VariableManager(loader=self._loader, inventory=self._inventory)
        self._dynamic_inventory()

    def _add_dynamic_group(self, hosts_list, groupname, groupvars=None, cluster=None):
        """
        动态添加主机到指定的主机组
        :param hosts_list: 主机列表 [{"ip": "192.168.100.10", "port": "22", "username": "root", "password": None}, {}]
        :param groupname:  组名称
        :param groupvars:  组变量，格式为字典
        :param cluster:  先前集群信息，字典列表
        :return:
        """
        # 添加组
        my_group = self._inventory.add_group(groupname)
        pre_group = self._inventory.add_group("pregroup")

        # 添加组变量
        if groupvars:
            for key, value in groupvars.items():
                self._inventory._inventory.set_variable(my_group, key, value)
                # my_group.set_variable(key, value)
        if cluster:
            # print(cluster)
            setcluster = sorted(cluster["clustervalue"])
            # print(setcluster)
            self._inventory._inventory.set_variable(my_group, "pre_clusters", setcluster)
            # pre_group = self._inventory.add_group("pregroup")
            for i in setcluster:
                hostip = i.split(':')[0]
                self._inventory.add_host(hostip, "pregroup")
                username = i.split(':')[2]
                password = i.split(':')[3]
                sshport = i.split(':')[1]
                installpath = i.split(':')[-1]
                self._inventory._inventory.set_variable(hostip, "ansible_ssh_host", hostip)
                self._inventory._inventory.set_variable(hostip, "ansible_ssh_port", sshport)
                self._inventory._inventory.set_variable(hostip, "ansible_ssh_user", username)
                self._inventory._inventory.set_variable(hostip, "ansible_ssh_pass", password)
                self._inventory._inventory.set_variable(hostip, "inspath", installpath)
                if cluster["clustertype"] == "flink":
                    jmip = i.split(':')[-2]
                    self._inventory._inventory.set_variable(hostip, "jmip", jmip)

        allhosts = []  # 记录所有主机生成seed供安装集群时使用
        # 添加一个主机
        print(hosts_list)
        hosts_list = sorted(hosts_list, key=lambda i: i["ip"])
        for host in hosts_list:
            hostname = host.get("hostname", None)
            hostip = host.get("ip", None)
            allhosts.append(hostip)
            if hostip is None:
                print("IP地址为空，跳过该元素。")
                continue
            hostport = host.get("port", "22")
            username = host.get("username", "root")
            password = host.get("password", None)
            ssh_key = host.get("ssh_key", None)
            python_interpreter = host.get("python_interpreter", None)

            try:
                # hostname可以不写，如果为空默认就是IP地址
                if hostname is None:
                    hostname = hostip
                # 添加主机到组
                self._inventory.add_host(hostip, groupname)
                # 添加主机变量
                self._inventory._inventory.set_variable(hostip, "ansible_ssh_host", hostip)
                self._inventory._inventory.set_variable(hostip, "hostname", hostname)
                self._inventory._inventory.set_variable(hostip, "ansible_ssh_port", hostport)
                self._inventory._inventory.set_variable(hostip, "ansible_ssh_user", username)
                if password:
                    self._inventory._inventory.set_variable(hostip, "ansible_ssh_pass", password)
                if ssh_key:
                    self._inventory._inventory.set_variable(hostip, "ansible_ssh_private_key_file", ssh_key)
                if python_interpreter:
                    self._inventory._inventory.set_variable(hostip, "ansible_python_interpreter", python_interpreter)

                # 添加其他变量
                for key, value in host.items():
                    if key not in ["ip", "hostname", "port", "username", "password", "ssh_key", "python_interpreter"]:
                        self._inventory._inventory.set_variable(hostip, key, value)

            except Exception as err:
                print(err)
        allhosts = sorted(allhosts)
        self._inventory._inventory.set_variable(my_group, "seed_hosts", allhosts)
        self._inventory._inventory.set_variable(pre_group, "flink_hosts", allhosts)
        self._inventory._inventory.set_variable(my_group, "firstnode", allhosts[0])
        if len(allhosts) > 1:
            self._inventory._inventory.set_variable(my_group, "secondnode", allhosts[1])
        # if pre_group:
        self._inventory.add_host(allhosts[0], "pregroup")
        self._inventory._inventory.set_variable(pre_group, "excludenode", allhosts[0])

    def _dynamic_inventory(self):
        """
        添加 hosts 到inventory
        :return:
        """
        if isinstance(self._hostsresource, list):
            self._add_dynamic_group(self._hostsresource, "groups")
        elif isinstance(self._hostsresource, dict):
            print("dict")
            for groupname, hosts_and_vars in self._hostsresource.items():
                if "cluster" in hosts_and_vars.keys():
                    self._add_dynamic_group(hosts_and_vars.get("hosts"), groupname, hosts_and_vars.get("vars"),
                                            hosts_and_vars.get("cluster"))
                else:
                    self._add_dynamic_group(hosts_and_vars.get("hosts"), groupname, hosts_and_vars.get("vars"),
                                            cluster=None)

    @property
    def INVENTORY(self):
        """
        返回资产实例
        :return:
        """
        return self._inventory

    @property
    def VARIABLE_MANAGER(self):
        """
        返回变量管理器实例
        :return:
        """
        return self._variable_manager


class AnsibleAPI:
    """
    初始化ansible的相关对象及参数
    """

    def __init__(self, hostsresource, sources):
        """
        可以选择性的针对业务场景在初始化中加入用户定义的参数
        """
        self._passwords = dict(sshpass=None, becomepass=None)
        self._loader = DataLoader()
        myinven = MyInventory(hostsresource, sources)
        self._inventory = myinven.INVENTORY
        print(self._inventory.groups)
        self._variable_manager = myinven.VARIABLE_MANAGER
        self.callback = None
        self.__init_options()

    def __init_options(self):
        """
        自定义选项，不用默认值的话可以加入到__init__的参数中
        :return:
        """
        # constants里面可以找到这些参数，ImmutableDict代替了较老的版本的nametuple的方式
        context.CLIARGS = ImmutableDict(
            connection="smart",
            remote_user="root",
            ack_pass=None,
            sudo=True,
            sudo_user="root",
            ask_sudo_pass=False,
            module_path=None,
            become=True,
            become_method="sudo",
            become_user="root",
            check=False,
            listhosts=None,
            listtasks=None,
            listtags=None,
            syntax=None,
            diff=True,
            subset=None,
            timeout=10,
            private_key_file="/root/.ssh/id_rsa",
            host_key_checking=False,
            forks=4,
            # 当使用代理是此处ssh设置
            # ssh_common_args='-o StrictHostKeyChecking=no -o ProxyCommand="ssh -W %h:%p -p 22 -q 192.168.181.131"', # 代理设置
            ssh_common_args='-o StrictHostKeyChecking=no',
            ssh_extra_args='-o StrictHostKeyChecking=no',
            verbosity=0,
            start_at_task=None,
        )

    def run_playbook(self, playbook_yml, extra_vars=None):
        print(playbook_yml)
        print(self._inventory.groups.get("groups").get_hosts())
        try:
            self.callback = PlaybookCallbackModule()
            if extra_vars:
                self.variable_manager.extra_vars = extra_vars
            executor = PlaybookExecutor(
                playbooks=[playbook_yml], inventory=self._inventory, variable_manager=self._variable_manager,
                loader=self._loader,
                passwords=self._passwords,
            )
            executor._tqm._stdout_callback = self.callback
            executor.run()
            print('over')
        except Exception as e:
            return False

    def run_module(self, module_name, module_args, hosts=None):
        play_source = dict(
            name="Run Module",
            hosts=hosts,
            gather_facts='no',
            tasks=[
                {"action": {"module": module_name, "args": module_args}},
            ]
        )
        play = Play().load(play_source, variable_manager=self._variable_manager, loader=self._loader)
        tqm = None
        self.callback = ResuCallbackModule()
        try:
            tqm = TaskQueueManager(
                inventory=self._inventory,
                variable_manager=self._variable_manager,
                loader=self._loader,
                passwords=self._passwords,
            )
            tqm._stdout_callback = self.callback
            tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()
            # 这个临时目录会在 ~/.ansible/tmp/ 目录下
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

    def get_run_result(self):
        result_raw = {'success': {}, 'failed': {}, 'unreachable': {}}
        for host, result in self.callback.host_ok.items():
            result_raw['success'][host] = result._result["rc"]
        for host, result in self.callback.host_failed.items():
            result_raw['failed'][host] = result._result
        for host, result in self.callback.host_unreachable.items():
            result_raw['unreachable'][host] = result._result

        # 最终打印结果，并且使用 JSON 继续格式化
        print(json.dumps(result_raw, indent=4))

    def get_play_result(self):
        results_raw = {'skipped': {}, 'failed': {}, 'ok': {}, "status": {}, 'unreachable': {}, "changed": {},
                       "espass": {}}
        print('123')
        for host, result in self.callback.host_ok.items():
            results_raw['ok'][host] = result

        for host, result in self.callback.host_failed.items():
            results_raw['failed'][host] = result

        # for host, result in self.callback.host_status.items():
        #    results_raw['status'][host] = result
        # print('status', self.results_raw)

        # for host, result in self.callback.host_changed.items():
        #    results_raw['changed'][host] = result
        # print('changed', self.results_raw)

        for host, result in self.callback.host_skipped.items():
            results_raw['skipped'][host] = result

        for host, result in self.callback.host_unreachable.items():
            results_raw['unreachable'][host] = result
        results_raw['espass'] = self.callback.host_password
        print(json.dumps(results_raw, indent=4))
        return json.dumps(results_raw, indent=4)
        # print(json.dumps(results_raw, indent=4))


def main():
    hosts_dict = {
        "groups": {
            "hosts": [{"ip": "192.168.181.129", "port": "22", "username": "root", "password": None, "var1": "host"},
                      {"ip": "192.168.181.79", "port": "22", "username": "root", "password": None, "var1": "host1"}],
            "vars": {"var2": "ansible"}
        }
    }

    playbook_yml = sys.argv[1]
    hostsresource = eval(sys.argv[2])
    # get current group's host
    rbt = AnsibleAPI(hostsresource, sources=None)
    # print(rbt._inventory.groups)
    # print(rbt._inventory.groups.get("pregroup").get_hosts())
    # print(rbt._inventory.groups.get("pregroup").get_vars())
    # print(rbt._inventory.hosts.get("192.168.95.114").get_vars())
    # rbt.run_module(module_name='command', module_args='pwd', hosts=["groups"])

    rbt.run_playbook(playbook_yml=playbook_yml)

    rbt.get_play_result()


if __name__ == "__main__":
    try:
        main()
    finally:
        sys.exit()
