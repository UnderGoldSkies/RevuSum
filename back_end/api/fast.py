import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from taxifare.ml_logic.preprocessor import preprocess_features
from taxifare.ml_logic.registry import load_model

app = FastAPI()
#load model at the beginning in the cache
model = load_model()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# http://127.0.0.1:8000/predict?pickup_datetime=2012-10-06 12:10:20&pickup_longitude=40.7614327&pickup_latitude=-73.9798156&dropoff_longitude=40.6513111&dropoff_latitude=-73.8803331&passenger_count=2
@app.get("/predict")
def predict(
        pickup_datetime: str,  # 2013-07-06 17:18:00
        pickup_longitude: float,    # -73.950655
        pickup_latitude: float,     # 40.783282
        dropoff_longitude: float,   # -73.984365
        dropoff_latitude: float,    # 40.769802
        passenger_count: int        # 1
    ):
    """
    Make a single course prediction.
    Assumes `pickup_datetime` is provided as a string by the user in "%Y-%m-%d %H:%M:%S" format
    Assumes `pickup_datetime` implicitly refers to the "US/Eastern" timezone (as any user in New York City would naturally write)
    """
    #convert to pandas dataframe
    # df = pd.DataFrame({'pickup_datetime': pickup_datetime,
    #                        'pickup_longitude': pickup_longitude,
    #                        'pickup_latitude': pickup_latitude,
    #                        'dropoff_longitude': dropoff_longitude,
    #                        'dropoff_latitude': dropoff_latitude,
    #                        'passenger_count': passenger_count
    #                       })
    DTYPES_RAW = {
    "pickup_datetime": "datetime64[ns, UTC]",
    "pickup_longitude": "float32",
    "pickup_latitude": "float32",
    "dropoff_longitude": "float32",
    "dropoff_latitude": "float32",
    "passenger_count": "int16"
    }
    new = [[pickup_datetime, pickup_longitude, pickup_latitude,
           dropoff_latitude, dropoff_longitude, passenger_count]]
    cols = ['pickup_datetime', 'pickup_longitude', 'pickup_latitude',
            'dropoff_latitude', 'dropoff_longitude', 'passenger_count']
    df= pd.DataFrame(new, columns=cols)
    df = df.astype(DTYPES_RAW)
    X_pred = preprocess_features(df)

    y= model.predict(X_pred)

    return {'fare_amount': float(y)}


@app.get("/")
def root():
    return {'greeting': 'Kevin'}
