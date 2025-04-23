import React from 'react';
import Modal from 'react-modal';
import { useState, useRef, useEffect } from 'react';

const IdModal = ({ setId, idModalIsOpen, closeIdModal }) => {

  const [idValue, setValue] = useState(null);
  const [error, setError] = useState("");

  const customStyles = {
    overlay: {
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
    },
    content: {
      top: '50%',
      left: '50%',
      right: 'auto',
      bottom: 'auto',
      marginRight: '-50%',
      transform: 'translate(-50%, -50%)',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      gap: '20px',
      textAlign: 'center',
      borderRadius: '15px',
      border: 'none',
      filter: 'drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25))',
      padding: '25px 30px',
      maxWidth: '500px',
      minWidth: '380px'
    },
  };

  const registerId = (event) => {
    event.preventDefault();
    if (!idValue || idValue === "") {
      setError("ID field cannot be empty");
    } else if (!Number.isInteger(Number(idValue))) {
      setError("ID must be an integer");
    } else if (Number.isInteger(Number(idValue)) && parseInt(idValue) <= 0) {
      setError("ID must be a positive number");
    } else if (Number.isInteger(Number(idValue))) {
      setId(parseInt(idValue));
      closeIdModal();
    }
  };

  return (
    <Modal
      isOpen={idModalIsOpen}
      onRequestClose={closeIdModal}
      style={customStyles}
      shouldCloseOnOverlayClick={false}
    >
      <p className='id-info'>
        Please insert your participant ID and press continue.
        <br/>The ID has been sent to you via email.
      </p>
      {error && error !== "" && <p className='error-message'>{error}</p>}
      <form onSubmit={registerId} className="id-input">
        <div className="input-label-container">
          <label for="id"><h3>ID</h3></label>
          <input
            id="id"
            name="id"
            type="text"
            value={idValue}
            onChange={(event) => setValue(event.target.value)}
          />
        </div>
        <button 
          type="button"
          className="topic-submit-btn"
          onClick={registerId}>
          Continue 
        </button>
      </form>
    </Modal>
  );
};

export default IdModal;
  