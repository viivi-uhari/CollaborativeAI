import { useState, useRef, useEffect } from 'react';
import Header from "./components/Header";
import Footer from "./components/Footer";
import FinishButton from './components/FinishButton';
import FeedbackForm from "./components/FeedbackForm";
import Workspace from "./components/Workspace";
import ConversationDisplay from "./components/ConversationDisplay";
import TaskDescription from './components/TaskDescription';
import ThemeForm from './components/ThemeForm';
import "./index.css";

const App = () => {
  const [isFinished, setIsFinished] = useState(false); 
  const [isFinishClicked, setIsFinishClicked] = useState(false);
  const [isRatingSubmitted, setIsRatingSubmitted] = useState(false);
  const viewPointRef = useRef(null);

  const [topic, setTopic] = useState("");
  const [format, setFormat] = useState("");
  const [number, setNumber] = useState(1);
  const [isDisabled, setIsDisabled] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  
  useEffect(() => {
    if (isFinished) {
      if (viewPointRef.current) {
        viewPointRef.current.scrollIntoView({ behavior: "smooth", block: "center"});
      }
    }
  }, [isFinished]);

  const toggleFinish = () => {
    setIsFinished(!isFinished);
    setIsFinishClicked(!isFinishClicked);
  }
  
  return (
    <>
      <Header />
      <TaskDescription/>
      <ThemeForm 
        topic={topic} setTopic={setTopic} 
        format={format} setFormat={setFormat} 
        number={number} setNumber={setNumber} 
        isDisabled={isDisabled} 
        setIsDisabled={setIsDisabled} 
        setIsLoading={setIsLoading}
      />
      <div className="main-interaction">
        {(isRatingSubmitted || isFinishClicked) && (
          <div className="main-interaction-overlay"> </div>
        )}
        <Workspace />
        <ConversationDisplay />
      </div>
      <FinishButton isFinishClicked={isFinishClicked} isRatingSubmitted={isRatingSubmitted} toggleFinish={toggleFinish} />
      {isFinished && <FeedbackForm viewPointRef={viewPointRef} isRatingSubmitted={isRatingSubmitted} setIsRatingSubmitted={setIsRatingSubmitted}/>}
      <Footer />
    </>
  );
};

export default App;
