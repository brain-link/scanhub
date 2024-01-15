Software Requirement Specification (SWRS)
#########################################

!! This Section is Work in Progress. !!

Functional Requirements
=======================

+--------------+-------------+------------+--------------+
|      ID      | Requirement | Acceptance | Traceability |
+==============+=============+============+==============+
| SWRS_FR_0001 | TBD         | TBD        | TBD          |
+--------------+-------------+------------+--------------+
| SWRS_FR_0002 | TBD         | TBD        | TBD          |
+--------------+-------------+------------+--------------+


Device Communication
====================

Acquisition Request
-------------------

The following information shall be communicated with an acquisition request to specify modality specific instructions/commands.
Authentification and authorization topics are left out for now.

Request:

- **device-id:** Double check if request was communicated to the right device
- **command:** Start, stop, pause, ...
- **parameters:** Key-value pairs, can be simple values, instruction files or a combination of both, device limits
- **record-id:** ID which is assigned per initial request and traced from record creation to the last workflow step, gives access to job-id (may be extended by additional trace ID)
- **device-authentication-key:** TBD

Response: HTTPS_RESPONSE


**Communication Flow**

(Replace by better formatting)

    UI 
    
    -> Acquisition Control

        -> Request acquisition command/parameters (sequence manager)

        -> create record (exam manager) 

        -> get device (device manager)

    -> Device (acquisition request) 
    
    -> Workflow Manager 
    
    -> Workflows


**MR-Domain Model**

(To be moved to SWAD)
JSON payload which is communicated from acquisition control to device (MRI acquisition request).
The following example is


.. code-block:: javascript
    :linenos:

    device_id: str,
    command: enum, // start, stop, pause
    parameters: {
        context: str, // content of a sequence file (can be pulseq)
        format: enum, // pulseq, ocra, ...
        acqusition_limits: {
            // parameters used to calculate SAR, double check for completeness
            patient_height: float,
            patient_weight: float,
            patient_gender: enum,
            patient_age: int,
        },
        sequence_parameters: {
            // User input for MRI console to execute the sequence properly, for now only fov.
            // Note: The following section is specific to the format (here pulseq). 
            // It may vary for different sequence formats and thus should be 
            // implemented as a generic dictionary inside a pydantic MR domain model.
            fov: [
                float, 
                float, 
                float
            ],
            fov_offset: [
                float, 
                float, 
                float
            ]
        }
    }


Device Monitor
--------------

Monitoring of device status through direct connection between device and device manager.
Get the current device status: connected, disconnected, scanning, etc.
    
    TODO: What are possible device status?

The device status is to be implemented as an enum with defined situations (see above).


Device Configuration
--------------------

This set of parameters is specific to one device. Read and/or write requests are performed through the device manager.
Some parameters are fixed limits and cannot be modified by the device manager (`system_limits`).
Another set of parameters may vary over time and may be set from a workflow/workflow-step result (`current_device_configuration`).

.. code-block:: javascript
    :linenos:

    
    system_limits: {
    // hard system limits (read only)
        max_gradients: [
            float, 
            float, 
            float
        ],
        max_rf_duration: float,
        adc_deadtime: float,
        rf_dead_time: float,
        // ...
    },
    current_device_configuration: {
    // temporary system values (read and write)
        larmor_frequency: float,
        flip_angle_calibration: float,
        gradient_calibration: [
            float, 
            float, 
            float
        ],
        gradient_offset: [
            float, 
            float, 
            float
        ],
        // ...
    }




