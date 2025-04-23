const Feedback = ({ elapsedTime }) => {

  return (
    <div className="feedback-container">
      <h3>Task completed in: {Math.round(elapsedTime/60)} minutes</h3>
      <h3>
        Thank you, for taking the time to complete the collaborative task!<br/>
        Now please fill out the following questionnaire while keeping this tab open (the link will open in a separate tab):
      </h3>
      <a href="https://link.webropolsurveys.com/S/828BAA4F4D3FC7C1" target="_blank">Post-task questionnaire</a>
      <p>After you have filled out the questionnaire, we will register that you have completed the study, and you will receive your monetary compensation shortly.</p>
    </div>
  );
};

export default Feedback;
