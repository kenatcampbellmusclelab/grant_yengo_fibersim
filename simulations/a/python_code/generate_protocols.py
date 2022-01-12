# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 18:59:35 2022

@author: kscamp3
"""

import sys
import os
import json

import pathlib

import numpy as np


def write_protocols():
    """ Writes a sequence of protocols to a directory structure """
    
    # Variables
    FiberPy_protocol_path = 'c:/ken/github/campbellmusclelab/models/fibersim/code/fiberpy/fiberpy/package/modules/protocols'
    base_directory = '..'
    batch_file_string = '../batch_temp.json'

    # Finds path for FiberPy and provides access to protocol utilities
    sys.path.append(FiberPy_protocol_path)
    import protocols

    # Create a batch
    FiberSim_batch = dict()
    FiberSim_batch['job'] = []
    
    # Define number of models
    no_of_models = 4
    
    # Define the isometric pCa values
    isometric_pCa_values = np.concatenate(([8.0], np.arange(6.4, 5.0, -0.2), [4.6]))
    
    # And the isotonic forces
    # isotonic_forces = np.logspace(np.log10(2000), np.log10(90000), 10)
    isotonic_forces = np.linspace(2000, 110000, 10)
    
    for m in range(no_of_models):
        for pCa in isometric_pCa_values:
            
            # Generate the file string
            prot_file_string = os.path.join(base_directory,
                                            'sim_input',
                                            ('%i' % (m+1)),
                                            'isometric',
                                            ('pCa_%.0f' % (10*pCa)),
                                            ('prot.txt'))
            
            # Generate the protocol
            prot = protocols.create_length_control_protocol(step_pCa=pCa,
                                                            step_pCa_s = 0.01,
                                                            n_points=1000)
            
            # Write protocol to file
            protocols.write_protocol_to_file(prot, prot_file_string)
            
            # Add to batch
            job = dict()
            job['relative_to'] = "this_file"
            job['model_file'] = os.path.join('sim_input',
                                             ('%i' % (m+1)),
                                             ('model_%i.json' % (m+1)))
            job['options_file'] = os.path.join('sim_input',
                                               'sim_options.json')
            job['protocol_file'] = os.path.join(*prot_file_string.split('\\')[1:])
            job['results_file'] = os.path.join('sim_output',
                                               'isometric',
                                               ('%i' % (m+1)),
                                               ('pCa_%.0f_results.txt' % (10*pCa)))
            job['output_handler_file'] = os.path.join('sim_input',
                                                      ('%i' % (m+1)),
                                                      'isometric',
                                                      ('pCa_%.0f' % (10*pCa)),
                                                      'output_handler.json')
            
            FiberSim_batch['job'].append(job)

            # Create the output handler
            output_handler = dict()
            output_handler['templated_images']=[]
            th = dict()
            th['relative_to'] = "this_file"
            th['template_file_string'] = "../../../../template/template_summary.json"
            th['output_file_string'] = os.path.join('../../../../sim_output',
                                                    'isometric',
                                                    ('%i' % (m+1)),
                                                    ('pCa_%.0f_summary.png' % (10*pCa)))
            output_handler['templated_images'].append(th)

            # Write output handler file
            output_handler_file = os.path.join(base_directory,
                                               job['output_handler_file'])
            parent_dir = os.path.dirname(output_handler_file)
            if not os.path.isdir(parent_dir):
                os.makedirs(parent_dir)
            with open(output_handler_file, 'w') as f:
                json.dump(output_handler, f, indent=4)

    for m in range(no_of_models):
        for i,iso_f in enumerate(isotonic_forces):
            
            # Generate the file string
            prot_file_string = os.path.join(base_directory,
                                            'sim_input',
                                            ('%i' % (m+1)),
                                            'isotonic',
                                            ('%i' % i),
                                            ('prot.txt'))
            
            # Generate the protocol
            prot = protocols.create_force_control_protocol(n_points=3000,
                                                           iso_start_s=0.2,
                                                           step_pCa=pCa,
                                                           iso_f=iso_f)
            
            # Write protocol to file
            protocols.write_protocol_to_file(prot, prot_file_string)
            
            # Add to batch
            job = dict()
            job['relative_to'] = "this_file"
            job['model_file'] = os.path.join('sim_input',
                                             ('%i' % (m+1)),
                                             ('model_%i.json' % (m+1)))
            job['options_file'] = os.path.join('sim_input',
                                               'sim_options.json')
            job['protocol_file'] = os.path.join(*prot_file_string.split('\\')[1:])
            job['results_file'] = os.path.join('sim_output',
                                               'isotonic',
                                               ('%i' % (m+1)),
                                               ('iso_%i_results.txt' % i))
            job['output_handler_file'] = os.path.join('sim_input',
                                                      ('%i' % (m+1)),
                                                      'isotonic',
                                                      ('%i' % i),
                                                      'output_handler.json')
            
            FiberSim_batch['job'].append(job)

            # Create the output handler
            output_handler = dict()
            output_handler['templated_images']=[]
            th = dict()
            th['relative_to'] = "this_file"
            th['template_file_string'] = "../../../../template/template_summary.json"
            th['output_file_string'] = os.path.join('../../../../sim_output',
                                                    'isotonic',
                                                    ('%i' % (m+1)),
                                                    ('iso_%i_summary.png' % i))
            output_handler['templated_images'].append(th)

            # Write output handler file
            output_handler_file = os.path.join(base_directory,
                                               job['output_handler_file'])
            parent_dir = os.path.dirname(output_handler_file)
            if not os.path.isdir(parent_dir):
                os.makedirs(parent_dir)
            with open(output_handler_file, 'w') as f:
                json.dump(output_handler, f, indent=4)
    
    # Write batch to file
    with open(batch_file_string, 'w') as f:
        json.dump(FiberSim_batch, f, indent=4)


if __name__ == "__main__":
    write_protocols()