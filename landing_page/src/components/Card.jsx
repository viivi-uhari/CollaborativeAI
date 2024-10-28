const Card = ({card}) => {
  return (
    <div className="card-container">
      <img src={card.link} alt={card.name} className="card-img"/>
      <h2 className="card-name">{card.name}</h2>
      <div className="card-description">
        <ul>
          {[... card.description].map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </div>
      <div className="card-btn-group">
        <div className="task-btn-wrapper">
          <a className="task-btn" type="button" href={card.task_link} style={{color: "rgb(176, 124, 124)"}}>
            <i className="fa fa-play"></i>       
          </a>
          <p className="task-link-text">Launch task</p>
        </div>
        <div className="code-btn-wrapper">
          <a className="code-btn" type="button" href={card.code_link} style={{color: "rgb(176, 124, 124)"}} >
            <i className="fa fa-code"></i>
          </a>
          <p className="code-link-text">View code</p>
        </div>
      </div>
    </div>
  );
}

export default Card;