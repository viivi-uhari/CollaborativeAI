const TopicSummary = ({ topic, format, number }) => {

  return (
    <div className="topic-summary">
      <b className="explanatory-warning-text">
        {number} {number > 1 ? "references" : "reference"} formatted in {format} for the topic:
      </b>
      <b className="explanatory-warning-text">"{topic}"</b>          
    </div>
  );
};

export default TopicSummary;
    