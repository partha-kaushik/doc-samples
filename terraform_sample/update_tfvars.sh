#!/bin/bash
# Updates ./gcpinstance.tfvars file with values from env-vars
# Env-vars can come from Jenkins pipeline parameters 
# or from the shell if terraform is being run from command-line
#
# After setting env-vars in the shell, invoke this script:
# update_tfvars.sh ./gcpinstance.tfvars
#
function updateTfvars () {
    file1="${1}";
    paramNames=( 'vcp_network_name' 'routing_mode');
    paramValues=( "${VPC_NAME}" "${ROUTING_MODE}"  );
    echo "Updating tfvars ... vm_template = ${vm_template}";
    i=0; nameValueSeparator=' = '
    while [ $i -lt ${#paramNames[@]} ]; do
        if [[ "${paramNames[i]}" == *list ]] ; then
            sed -i -e "/${paramNames[i]}/s/.*/${paramNames[i]}${nameValueSeparator}${paramValues[i]}/" ${file1};
        else
            sed -i -e "/${paramNames[i]}/s/.*/${paramNames[i]}${nameValueSeparator}\"${paramValues[i]}\"/" ${file1};
        fi
        if [[ "${paramNames[i]}" == *password  ]]; then value="*******"; else value="${paramValues[i]}"; fi
        echo "updated ${paramNames[i]} :: ${value}"
        ((i+=1))
    done
}