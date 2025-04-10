const FinalList = ({ finalList }) => {
  return (
    <div className="final-reference-list">
      {finalList
        .map((item, index) => (
          <p key={index}>{item}</p>
      ))}
    </div>
  );
};

export default FinalList;
