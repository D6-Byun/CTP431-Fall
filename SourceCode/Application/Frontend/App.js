import React, { useState, useEffect, useRef } from "react";
import axios from "axios";

const App = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [results, setResults] = useState([]);
  const [taskId, setTaskId] = useState(null);
  const [status, setStatus] = useState("");
  const [pollCount, setPollCount] = useState(0);
  const [processedAudio, setProcessedAudio] = useState(null);
  const [currentPrediction, setCurrentPrediction] = useState(""); // 현재 prediction_all 저장
  const audioRef = useRef(null); // audio 태그 참조

  const inst_pool = ['cel', 'cla', 'flu', 'gac', 'gel', 'org', 'pia', 'sax', 'tru', 'vio', 'voi'];

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post("http://127.0.0.1:5000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setTaskId(response.data.task_id);
      setStatus("Processing...");
      setPollCount(0);
      pollStatus(response.data.task_id);
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("File upload failed!");
    }
  };

  const pollStatus = async (taskId) => {
    const interval = setInterval(async () => {
      setPollCount((prevCount) => prevCount + 1);
      try {
        const response = await axios.get(`http://127.0.0.1:5000/status/${taskId}`);
        const taskStatus = response.data;

        if (taskStatus.status === "completed") {
          clearInterval(interval);
          setStatus("Completed!");
          setResults(taskStatus.results);
          setProcessedAudio(`http://127.0.0.1:5000/stream/${taskStatus.filename}`);
        } else if (taskStatus.status === "failed") {
          clearInterval(interval);
          setStatus("Failed: " + taskStatus.error);
        }
      } catch (error) {
        console.error("Error checking status:", error);
        clearInterval(interval);
        setStatus("Error checking task status.");
      }
    }, 5000);
  };

const updatePrediction = () => {
  if (!audioRef.current || !results.length) return;

  const currentTime = audioRef.current.currentTime;
  const index = Math.floor(currentTime / 3); // 3초 단위로 인덱스 계산
  if (index < results.length && results[index]?.prediction_all) {
    const mappedPredictions = results[index].prediction_all.map((value, idx) => {
      // value가 숫자인지 확인하고 처리
      const probability = typeof value === "number" ? value.toFixed(4) : "N/A";
      return {
        instrument: inst_pool[idx] || "Unknown", // inst_pool 범위를 초과하는 경우 처리
        probability,
      };
    });
    setCurrentPrediction(mappedPredictions);
  }
};


  useEffect(() => {
    const audio = audioRef.current;

    if (audio) {
      // 재생 시간이 업데이트될 때마다 prediction 갱신
      audio.addEventListener("timeupdate", updatePrediction);
      return () => {
        audio.removeEventListener("timeupdate", updatePrediction);
      };
    }
  }, [results]); // results가 업데이트될 때 이벤트 핸들러 등록

  return (
    <div>
      <h1>Audio Processor</h1>
      <div>
        <input type="file" accept=".wav, .mp3" onChange={handleFileChange} />
        <button onClick={handleUpload}>Upload and Process</button>
      </div>
      <div>
        <h3>
          Status: {status} {status === "Processing..." && `Polling.. ${pollCount}`}
        </h3>
        {processedAudio && (
          <div>
            <h3>Processed Audio:</h3>
            <audio controls ref={audioRef}>
              <source src={processedAudio} type="audio/wav" />
              Your browser does not support the audio element.
            </audio>
            <div>
              <h4>Current Prediction:</h4>
              {currentPrediction &&
                currentPrediction.map((pred, idx) => (
                  <p key={idx}>
                    {pred.instrument}: {pred.probability}
                  </p>
                ))}
            </div>
          </div>
        )}
        {results.map((result, index) => (
          <div key={index}>
            <h3>Predicted Class: {result.predicted_class}</h3>
            <img
              src={`data:image/jpeg;base64,${result.image}`}
              alt={`Spectrogram ${index}`}
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default App;
