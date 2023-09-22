# CardiacOutput_VTI_Synch
Scripts synchronizing hemodynamic metrics from a monitor and a wearable device and calculating the relationship between both metrics

### These scripts analyze and compare data collected using two different biomedical devices: a Monitor and a Wearable device


### The data was acquired duirng a Lower Body Negative Pressure Chamber (LBNP) Paradigm:
- Subjects lie down on bed, where subject’s lower body is place in the LBNP tank.
- Tank is air-tight sealed and provides sub-atmospheric pressure by a vacuum pump.
- After 5min of resting (baseline), continuous stepwise decrease in atmospheric pressure every 5min until - 50 mmHg or pre-syncope.


### Data acquisition properties:
- Monitor data is recorded continuously from start of session to the end with a sampling rate of 1000
- Wearable data recorded in a discontinuous manner with nonlinear sampling rate: time stamps correspond to detected start time of a beat.
- Wearable data recording start time is not necessarily at the same time Monitor data collection is started.
- Wearable data is labeled based on the pressure stage during which the recording was made (Baseline, Stage1, Stage 2). It is not confirmed when the start and end of the Wearable recording was made relative to pressure chamber stage changes.
- Common metric between 2 datasets: Heart rate (HR)
- Metrics to compare: Cardiac output (CO) and Velocity time integral (VTI)


### These scripts deliver the following results:
- Automatically establish synchronicity between the two datasets
- Updated and continuous time stamps for Wearable data (or required time shifts for data from each stage)
- Plots showing time-aligned Monitor and Wearable data
- Statistical analysis performed to understand whether there is a relationship between Monitor’s CO and Wearable’s VTI metrics.values from the 2 devices.
- Results from statistical analysis summarized in tabular format
- Plots and diagrams showing the relationship (or lack thereof) between the two analyzed metrics.
- Scripts for performing statistical analyses
