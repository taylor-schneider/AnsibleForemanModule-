import yaml

from unittest import TestCase


class Test_AnsibleFormanModule(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = "admin"
        self.password = "password"
        self.apiUrl = "https://15.4.7.1"
        self.verifySsl = False
        self.moduleName = "AnsibleForemanModule"

    def _PlaybookTemplate(self):
        playbookYaml = """
        - hosts: localhost
          remote_user: root
          tasks:
          - set_fact: my_global_var='hello'
          - name: "Re-run setup to use custom facts"
            setup: ~
          - name : "This is my task to execute my module"
            {0}:
              apiUrl : '{1}'
              username : '{2}'
              password : '{3}'
              verifyssl: {4}
              apiEndpoint : '{5}'
              httpMethod : '{6}'
              desiredState : {7}
            """

        return playbookYaml

    def _DesiredStateToPlaybookYaml(self, desiredState):

        desiredStateYaml = yaml.dump(desiredState, default_flow_style=False)
        paddedYaml = ""
        for line in desiredStateYaml.split("\n"):
            paddedYaml += "                " + line + "\n"
        return "\n" + paddedYaml

    def _GeneratePlaybook(self, moduleName, apiUrl, username, password, verifySsl, apiEndpoint, httpMethod, desiredState):

        template = self._PlaybookTemplate()

        paddedDesiredStateYaml = self._DesiredStateToPlaybookYaml(desiredState)

        playbook = template.format(moduleName, apiUrl, username, password, verifySsl, apiEndpoint, httpMethod, paddedDesiredStateYaml)
        return playbook

    def test_Main_EnsureEnvironmentExists_Success(self):
        apiEndpoint = "/api/environments"
        httpMethod = "post"
        desiredState =  {
            "environment": {
                "name": "some_environment"
            }
        }

        playbookYaml = self._GeneratePlaybook(
            self.moduleName,
            self.apiUrl,
            self.username,
            self.password,
            self.verifySsl,
            apiEndpoint,
            httpMethod,
            desiredState)

        s = ""
