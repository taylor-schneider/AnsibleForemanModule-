# Foreman Templates
Foreman uses a templating system to generate the files associated with PXE booting etc. In order to test the API I have created these template tests.
## How to use the templates
As part of the test suite, there are a set of ansible playbooks which will configure Foreman to pxe bot hosts. These playbooks rely on these files being made available by an http server. They will be pulled from the http server and installed into foreman.