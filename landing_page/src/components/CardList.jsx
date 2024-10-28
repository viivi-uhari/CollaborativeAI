import { useState } from "react";
import Card from "./Card";

const CardList = () => {
  const [cards, setCards] = useState([
    {
      name: "Tangram task",
      description: ["Compose an object with AI", "Coordination"],
      link: "./tg.png",
      task_link: "https://tangramtask1-tangram.node01.ki-lab.nrw/",
      code_link:
        "https://github.com/AaltoRSE/CollaborativeAI/tree/main/task_template/frontend_tangram",
    },
    {
      name: "Poetry task",
      description: ["Write a short poem with AI", "Co-creativity"],
      link: "./pt.png",
      task_link: "https://poetrytask1-poetry.node01.ki-lab.nrw/",
      code_link:
        "https://github.com/AaltoRSE/CollaborativeAI/tree/main/task_template/frontend_poetry",
    },
    {
      name: "Gesture task",
      description: ["TBA"],
      task_link: "#",
      code_link: "#",
    },
  ]);

  return (
    <div className="card-list">
      <div className="card-list-inner-border">
        {cards.map((card, index) => (
          <Card key={index} card={card} />
        ))}
      </div>
    </div>
  );
};

export default CardList;
