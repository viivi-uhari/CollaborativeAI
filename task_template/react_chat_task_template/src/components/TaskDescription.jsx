const TaskDescription = () => {
  return (
    <div className="task-description">
      <h2 className="task-title">Reference List Creation</h2>
      <h3 className="instructions-heading">Instructions</h3>
      <ol>
        <li>Provide the following information:</li> 
          <ul>
            <li className="ul-list-item">The topic you would like to find references to. Select one from the provided list.</li>
            <li className="ul-list-item">The citation format for the reference list.</li>
            <li className="ul-list-item">The number of references you would want.</li>
          </ul>
        <li>The AI then provides you with a possible list containing reference list citations in addition to information about the references.</li>
        <li>If you want to replace some of the references with new ones, you can communicate this to the AI.</li>
        <li>If you are satisfied with the references, you should communicate this to the AI.</li>
        <li>When you are satisfied with every reference, the AI will provide you with a final reference list formatted to the citation style you specified.</li>
      </ol>
    </div>
  );
};

export default TaskDescription;
