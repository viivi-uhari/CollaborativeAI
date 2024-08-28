import { useState } from 'react';
import Card from "./Card";

const CardList = () => {
  const [cards, setCards] = useState([
    {
      name: "Tangram task",
      description: "Make a tangram shape with the help of AI models",
      link: "./tg.png",
      task_link: "#",
      code_link: "https://github.com/AaltoRSE/CollaborativeAI/tree/main/task_template/frontend_tangram"
    },
    {
      name: "Poetry task",
      description: "Choose a topic and collaborate with AI models to create a poem",
      link: "./pt.png",
      task_link: "#",
      code_link: "https://github.com/AaltoRSE/CollaborativeAI/tree/main/task_template/frontend_poetry"
    },
    {
      name: "Gesture task",
      description: "TBA",
      task_link: "#",
      code_link: "#"
    }
  ]);

  return (
    <div className="card-list">
      <div className='card-list-inner-border'>
        {cards.map((card, index) => (
          <Card key={index} card={card} /> 
        ))}
      </div>
    </div>
  );
};

export default CardList;
