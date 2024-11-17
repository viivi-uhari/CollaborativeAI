import { useState } from "react";

const TutorialPopUp = () => {
  const [isOpen, setIsOpen] = useState(false);

  const togglePopUp = () => {
    setIsOpen(!isOpen)
  }

  return (
    <div>
      <button className="open-tutorial-btn" onClick={togglePopUp}>Quick guide</button>

      {isOpen && (
        <div className="popup-wrapper">
          <div className="popup">
            <button className="close-popup-btn" onClick={togglePopUp}>x</button>
            <h2>Poetry task quick guide</h2>
            <div className="image-grid-container">
              <div className="image-container">
                <img src="./intro.png" alt="Main UI" className="image" />
                <div className="description">
                  <p>
                    The main UI of the task. There are two interaction zones: 
                    "Your joint poem" shows the current poem and a form for you to submit your 
                    poemline while "Discussion with AI" shows the chat between you and the AI 
                    model and a form for you to send any comments or questions to it like a normal chat.
                  </p>
                </div>
              </div>

              <div className="image-container">
                <img src="./topic.png" alt="Choose your topic" className="image" />
                <div className="description">
                  <p>
                    First, you enter and submit the topic of the poem. After that, the AI model
                    will process and generate the first line of the poem. Then you and the AI take
                    turns to complete the poem. Meanwhile, you can chat with it in the
                    right-side box to raise any questions or suggestions. You can also request it
                    to generate the next poem line if you are stuck.
                  </p>
                </div>
              </div>

              <div className="image-container">
                <img src="./done.png" alt="Communicate with the AI model" className="image" />
                <div className="description">
                  <p>
                    When there are 9 lines of poem, the task is deemed completed. At the moment, the 
                    poem lines can be edited but it's purely just for the user to change/edit the content of 
                    the poem (nothing else happens when you save the change).
                  </p>
                </div>
              </div>

              <div className="image-container">
                <img src="./finish.png" alt="Send rating" className="image" />
                <div className="description">
                  <p>
                    Give the task a rating based on how well you and the AI model collaborated 
                    on the task. If you want to do the task again, you can press the redo button 
                    at the bottom.
                  </p>
                </div>
              </div>
              
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TutorialPopUp;
