## Does machine learning become more accurate as more data is provided?

See: https://qr.ae/pKkdtC

Generally speaking, yes, given that a few conditions are met:
The additional data is provided where the machine learning model (orange) needs it most. In the example below, you’re not going to see much improvement if you keep adding data to the tails (and ignoring the middle area).

![](./assets/adding_wrong_data_points.png)

Beware of “Garbage in - garbage out.” Do not compromise data quality just so that you have a larger dataset. Trading quality for quantity is never a winning bet in machine learning.

Furthermore, the ML model must have enough capacity to deal with the complexity of the underlying data. In the example below, adding more data will not improve accuracy since we’re attempting to model a nonlinear phenomenon with the wrong tool - linear regression.

![](./assets/inflexible_model.png)