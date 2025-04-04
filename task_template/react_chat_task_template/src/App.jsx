import { useState, useRef, useEffect } from 'react';
import Header from "./components/Header";
import Footer from "./components/Footer";
import FinishButton from './components/FinishButton';
import FeedbackForm from "./components/FeedbackForm";
import Dialogue from "./components/Dialogue";
import ConversationDisplay from "./components/ConversationDisplay";
import TaskDescription from './components/TaskDescription';
import VisualWarning from './components/VisualWarning';
import TopicSummary from './components/TopicSummary';
import TopicForm from './components/TopicForm';
import React from 'react';
import ReactDOM from 'react-dom';
import Modal from 'react-modal';
import constants from './constants/constants';
import "./index.css";
import ModalWarning from './components/ModalWarning';

const App = () => {
  const [isFinished, setIsFinished] = useState(false); 
  const [isFinishClicked, setIsFinishClicked] = useState(false);
  const [isRatingSubmitted, setIsRatingSubmitted] = useState(false);
  const viewPointRef = useRef(null);

  const [topic, setTopic] = useState(constants.topics[0]);
  const [format, setFormat] = useState("");
  const [number, setNumber] = useState(1);
  const [isDisabled, setIsDisabled] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const [references, setReferences] = useState([]);
  const [comments, setComments] = useState([]);

  const [currentWarning, setWarning] = useState(null);
  const [modalIsOpen, setIsOpen] = React.useState(true);

  function closeModal() {
    setIsOpen(false);
  }
  
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

  console.log(currentWarning);
  return (
    <>
      <Header />
      <TaskDescription/>
      {!isDisabled && <TopicForm 
        topic={topic} setTopic={setTopic} 
        format={format} setFormat={setFormat} 
        number={number} setNumber={setNumber} 
        isDisabled={isDisabled} 
        setIsDisabled={setIsDisabled} 
        setIsLoading={setIsLoading}
        setReferences={setReferences}
      />}
      {isDisabled && <TopicSummary topic={topic} format={format} number={number}/>}
       <VisualWarning
        modalIsOpen={modalIsOpen}
        closeModal={closeModal}
        currentWarning={currentWarning}
        setWarning={setWarning}/>
      
      <div className="main-interaction">
        {(isRatingSubmitted || isFinishClicked) && (
          <div className="main-interaction-overlay"> </div>
        )}
        <Dialogue isLoading={isLoading} setIsLoading={setIsLoading} references={references}/>
        <ConversationDisplay
          topic={topic}
          format={format}
          number={number}
          isDisabled={isDisabled} 
          setIsDisabled={setIsDisabled} 
          isLoading={isLoading} 
          setIsLoading={setIsLoading}
          comments={comments}
          setComments={setComments}
          references={references}
          setReferences={setReferences}
        />
      </div>
      <FinishButton isFinishClicked={isFinishClicked} isRatingSubmitted={isRatingSubmitted} toggleFinish={toggleFinish} />
      {isFinished && <FeedbackForm viewPointRef={viewPointRef} isRatingSubmitted={isRatingSubmitted} setIsRatingSubmitted={setIsRatingSubmitted}/>}
      <Footer />
    </>
  );
};

export default App;
