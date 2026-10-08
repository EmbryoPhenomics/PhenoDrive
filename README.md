# PhenoDrive

PhenoDrive is a platform for closing the loop between environmental control and organismal response - to dynamically adjust the environment an organism experiences on the basis of it's own biological response. Typical experiments are designed where environmental treatments are pre-determined, and the biological response to these is then measured after the fact. Future experimental treatments are then designed on the basis of these prior responses. PhenoDrive enables feedback between environmental control and phenotypic response, and therefore the experimental treatment can be adjusted dynamically over the course of an experiment, in response to biology, and towards a given objective, such as maximising growth during development. Below we describe a proof of concept of this particular objective.

## PhenoDrive enables real-time optimisation of growth in *Lymnaea stagnalis* embryos

Here we demonstrate an example of applying PhenoDrive to *Lymnaea stagnalis*, a model species in our lab, to optimise growth in relation to temperature, during embryonic development. *L. stagnalis* embryonic growth is characterised by a nonlinear process, with exponential growth in intermediate stages followed by a plateau in growth rate during the final stages as the embryo reaches the physical constraints of the egg capsule. 

The shape of this growth curve is largely preserved across different temperatures, with the entirety of development effectively squeezed into shorter timespans with increasing temperature, up until an optimum temperature whereafter the thermal stress of elevated temperature hinders embryonic development eventually leading to mortality.

![image](https://github.com/EmbryoPhenomics/PhenoDrive/blob/main/assets/growth_curves_two_temperatures.png)

We have characterised *L. stagnalis* embryonic development in relation to constant temperatures - where temperature is held at a fixed setpoint for the duration of the experiment - across a range of temperatures including the thermal optimum but also the upper critical thermal limits. Integrating these responses together produces the following heatmap:

![image](https://github.com/EmbryoPhenomics/PhenoDrive/blob/main/assets/growth_rate_landscape.png)


By integrating developmental rate and growth rate as a function of temperature, we can produce predictions for how long an embryo is likely to take to develop but also how much it will grow. We can therefore create forecasts for embryonic growth and validate those with empirical tests:

![image](https://github.com/EmbryoPhenomics/PhenoDrive/blob/main/assets/growth_prediction_22.5C.png)

By measuring growth in real-time as an embryo develops, we can produce forecasts dynamically and optimise towards the forecast most aligned with a particular objective, in this case maximising growth. Of course, individual variation brings added complexity, in that not all individuals respond the same. However, because PhenoDrive has feedback inherent in it's operation, any changes in phenotypic response can inform the environment created, as seen in the following experiment whereby an individual's growth rate began to decline and the system compensated by reducing temperature:

![image](https://github.com/EmbryoPhenomics/PhenoDrive/blob/main/assets/closed_loop_growth_to_hatch.gif)
