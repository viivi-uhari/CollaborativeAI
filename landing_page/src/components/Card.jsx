const Card = ({card}) => {
  return (
    <div className="card-container">
      <img src="https://picsum.photos/400/300" alt="card.name" className="card-img"/>
      <h2 className="card-name">{card.name}</h2>
      <p className="card-description">{card.description}</p>
      <div className="card-btn-group">
        <a class="link-btn" type="button" href={card.task_link}>
          <i class="fa fa-play"></i>        
        </a>
        <a class="code-btn" type="button" href={card.code_link}>
          <i class="fa fa-code"></i>
        </a>
      </div>
    </div>
  );
}

export default Card;