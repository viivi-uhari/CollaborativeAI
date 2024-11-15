import { useState } from 'react';
import ConversationDisplay from "./components/ConversationDisplay";
import Dialogue from "./components/Dialogue";
import TaskDescription from "./components/TaskDescription";
import Header from "./components/Header";
import Footer from "./components/Footer";
import FeedbackForm from "./components/FeedbackForm";
import TutorialPopUp from "./components/TutorialPopUp"
import "./index.css";

const App = () => {
  const [messages, setMessages] = useState([]);
  const [isFinished, setIsFinished] = useState(false);
  const [isFinishClicked, setIsFinishClicked] = useState(false);
  const [isDisabled, setIsDisabled] = useState(false);
  const [theme, setTheme] = useState("");

  const addMessage = (message) => {
    setMessages(prevMessages => prevMessages.concat(message));
  };

  const toggleFinish = () => {
    setIsFinished(!isFinished);
  };

  const toggleFinishButton = () => {
    toggleFinish();
    setIsFinishClicked(!isFinishClicked);
  }

  return (
    <>
      <Header />
      <TaskDescription />
      <div className="main-interaction">
        <Dialogue theme={theme} isDisabled={isDisabled} messages={messages} setMessages={setMessages} addMessage={addMessage} />
        <ConversationDisplay theme={theme} setTheme={setTheme} isDisabled={isDisabled} setIsDisabled={setIsDisabled} messages={messages} addMessage={addMessage} />
      </div>
      <div className="finish-btn-wrapper">
        <button type="submit" className="finish-btn" 
          disabled={messages.length <= 0}
          style={{
            "backgroundColor": isFinishClicked ? "#f44336" : "#6eb4ff",
            "cursor": isFinishClicked || messages.length <= 0 ? "not-allowed" : "pointer"
          }}
          onClick={toggleFinishButton}> 
          {isFinishClicked ? "Cancel" : "Rate task"}
        </button>
      </div>
      {isFinished && <FeedbackForm />}
      <Footer />
    </>
  );
};

export default App;
