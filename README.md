# FastAPI-ML-Docker 📦

## 🎯 Project Overview
This project demonstrates a core **MLOps** workflow: taking a trained Scikit-learn Machine Learning model, wrapping it in a **FastAPI** web service, and packaging the entire application into a portable **Docker** container.

This setup ensures that the ML model can be consistently deployed and run on any environment that supports Docker, eliminating "it works on my machine" problems.

---

## 🛠️ Tech Stack
* **Model:** Scikit-learn (Logistic Regression), packaged with `joblib`.
* **Serving API:** **FastAPI** (Python web framework)
* **Web Server:** **Uvicorn** (ASGI server for production)
* **Containerization:** **Docker**

---

## 📂 Project Structure
This structure assumes the `Dockerfile` was moved to the project root for the final successful build.

```mlops-docker-project/
├── app/
│   ├── main.py            # FastAPI service (loads model, defines endpoints)
│   └── requirements.txt   # Python dependencies for the container
├── model/
│   └── trained_model.pkl  # The trained Logistic Regression model artifact
├── .dockerignore          # Files to exclude from the Docker build context
├── Dockerfile             # Instructions for building the Docker image
└── README.md              # This documentation 
```

---

## 🚀 Building and Running the Service

### Prerequisites
1.  **Docker Desktop** (or Docker Engine) must be installed and running on your host machine.
2.  Your terminal must be open in the **root directory** of the project.

### Step 1: Build the Docker Image

This command reads the `Dockerfile` in the root and builds the image.

```bash
docker build -t iris-ml-service:v1 .
```

### Step 2: Run the Container
This command starts a new container instance in the background (-d), mapping the internal container port 80 to your host machine's port 8888.
```bash
docker run -d -p 8888:80 --name iris-predictor-container iris-ml-service:v1
```
### Step 3: Test the API
Confirm the service is running and predicting by sending a sample POST request.

**PowerShell Command:**
```powershell
# 1. Define the JSON body
$body = @{ 
    sepal_length = 5.1; 
    sepal_width = 3.5; 
    petal_length = 1.4; 
    petal_width = 0.2 
} | ConvertTo-Json

# 2. Send the request
Invoke-RestMethod -Uri http://localhost:8888/predict -Method POST -Headers @{"Content-Type" = "application/json"} -Body $body
```

**Expected Output:**
```bash
prediction_class confidence input_data                                                             
---------------- ---------- ----------                                                             
               0     0.9817 @{sepal_length=5.1; sepal_width=3.5; petal_length=1.4; petal_width=0.2}
```

## 🧹 Cleanup
Stop and remove the running container to free up system resources after testing.

**1. Stop the running container:**
```bash
docker stop iris-predictor-container
```
**2. Remove the stopped container instance:**

```bash
docker rm iris-predictor-container
```

**3. Remove the image (Optional - if no longer needed):**

```bash
docker rmi iris-ml-service:v1
```
