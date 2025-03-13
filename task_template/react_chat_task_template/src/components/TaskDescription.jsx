const TaskDescription = () => {
  return (
    <div className="task-description">
      <h2>Reference List Creation</h2>
      <h3>Instructions</h3>
      <ol>
        <li>Provide the following information:</li> 
          <ul>
            <li>A topic (related to your study field) you would like to find references to.</li>
            <li>The citation format for the reference list.</li>
            <li>The number of references you would want.</li>
          </ul>
        <li>The AI then provides you with a possible list containing refernec list citations in addition to information about the references.</li>
        <li>If you want to replace some of the refrences with new ones, you can communicate this to the AI.</li>
        <li>If you are satisfied with the references, you should communicate this to the AI.</li>
        <li>The AI will then provide you with a final reference list formatted to your preferred citation style.</li>
      </ol>
    </div>
  );
};

export default TaskDescription;
