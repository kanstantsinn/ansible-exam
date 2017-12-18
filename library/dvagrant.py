
import vagrant
from ansible.module_utils.basic import AnsibleModule
from pathlib import Path

def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        state=dict(type='str', required=True)
    )


    result = {}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
   

    file = open("invtmp", "w")
    file.close()

    
    my_file = Path("{}/Vagrantfile".format(module.params['path']))
    if not  my_file.is_file():
      module.fail_json(msg='The isnt Vagrantfile in directory', **result)

    v = vagrant.Vagrant(module.params['path'])
    if module.params['state'] == "started":
      v.up()
      result['path'] = module.params['path']
      result['state_vm'] = v.status()[0].state
      result['keyfile'] = v.keyfile()
      result['user'] = v.user()
      result['port'] = v.port() 
      k = v.ssh_config()
      p = k.split()
      result['ip_address'] = p[3]
      result['os_name'] = p[1]
      sss = v.ssh(command='free')
      result['RAM_size'] = sss.split()[7]

    elif module.params['state'] == "stopped":
      v.halt()
      result['state_vm'] = v.status()[0].state
    elif module.params['state'] == "destroyed":   
      v.destroy()
      result['state_vm'] = v.status()[0].state
    else:
      module.fail_json(msg='Dont allowed stated!!! allowed only: started, stopped, destroyed.', **result)
     
     
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
