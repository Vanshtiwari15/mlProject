from fastapi import FastAPI
from pydantic import BaseModel
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application = FastAPI()
app = application

# ✅ Pydantic model for request body
class InputData(BaseModel):
    gender: str
    ethnicity: str
    parental_level_of_education: str
    lunch: str
    test_preparation_course: str
    reading_score: float
    writing_score: float

# ✅ Simple root endpoint to test the API
@app.get("/")
def read_root():
    return {"message": "API is running. Send POST to /predictdata"}


# ✅ POST endpoint for prediction
@app.post("/predictdata")
def predict_data(input_data: InputData):
    # Use your CustomData class with input JSON
    data = CustomData(
        gender=input_data.gender,
        race_ethnicity=input_data.ethnicity,
        parental_level_of_education=input_data.parental_level_of_education,
        lunch=input_data.lunch,
        test_preparation_course=input_data.test_preparation_course,
        reading_score=input_data.reading_score,
        writing_score=input_data.writing_score,
    )

    pred_df = data.get_data_as_data_frame()

    predict_pipeline = PredictPipeline()
    results = predict_pipeline.predict(pred_df)

    return{"prediction": results[0]}