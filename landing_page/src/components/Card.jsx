const Card = ({card}) => {
  return (
    <div className="card-container">
      <img src={card.link} alt={card.name} className="card-img"/>
      <h2 className="card-name">{card.name}</h2>
      <p className="card-description">{card.description}</p>
      <div className="card-btn-group">
        <div className="task-btn-wrapper">
          <a class="task-btn" type="button" href={card.task_link} style={{color: "rgb(176, 124, 124)"}}>
            <i class="fa fa-play"></i>       
          </a>
          <p class="task-link-text">Launch task</p>
        </div>
        <div className="code-btn-wrapper">
          <a class="code-btn" type="button" href={card.code_link} style={{color: "rgb(176, 124, 124)"}} >
            <i class="fa fa-code"></i>
          </a>
          <p class="code-link-text">View code</p>
        </div>
      </div>
    </div>
  );
}

export default Card;