import React from 'react';
import Modal from 'react-modal';

const ModalWarning = ({ text, modalIsOpen, closeModal }) => {

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

  return (
    <Modal
      isOpen={modalIsOpen}
      onRequestClose={closeModal}
      style={customStyles}
      contentLabel="Example Modal"
    >
      <div className='warning-title'>
        <svg width="30" height="32" viewBox="0 0 30 32" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M13.2411 6.24957C13.9974 4.85226 16.0026 4.85226 16.7589 6.24957L26.3926 24.048C27.1138 25.3806 26.1489 27 24.6337 27H5.36632C3.85106 27 2.88616 25.3806 3.60745 24.048L13.2411 6.24957Z" fill="#FFA100"/>
          <path d="M16.2551 13.1818L16.0682 20.0565H14.3136L14.1218 13.1818H16.2551ZM15.1909 23.1246C14.8745 23.1246 14.6028 23.0128 14.3759 22.7891C14.149 22.5621 14.0371 22.2905 14.0403 21.9741C14.0371 21.6609 14.149 21.3924 14.3759 21.1687C14.6028 20.945 14.8745 20.8331 15.1909 20.8331C15.4945 20.8331 15.7614 20.945 15.9915 21.1687C16.2216 21.3924 16.3382 21.6609 16.3414 21.9741C16.3382 22.185 16.2823 22.3784 16.1737 22.5542C16.0682 22.7267 15.9292 22.8658 15.7566 22.9712C15.584 23.0735 15.3954 23.1246 15.1909 23.1246Z" fill="white"/>
        </svg>
        <h3>Warning</h3>
        <svg width="30" height="32" viewBox="0 0 30 32" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M13.2411 6.24957C13.9974 4.85226 16.0026 4.85226 16.7589 6.24957L26.3926 24.048C27.1138 25.3806 26.1489 27 24.6337 27H5.36632C3.85106 27 2.88616 25.3806 3.60745 24.048L13.2411 6.24957Z" fill="#FFA100"/>
          <path d="M16.2551 13.1818L16.0682 20.0565H14.3136L14.1218 13.1818H16.2551ZM15.1909 23.1246C14.8745 23.1246 14.6028 23.0128 14.3759 22.7891C14.149 22.5621 14.0371 22.2905 14.0403 21.9741C14.0371 21.6609 14.149 21.3924 14.3759 21.1687C14.6028 20.945 14.8745 20.8331 15.1909 20.8331C15.4945 20.8331 15.7614 20.945 15.9915 21.1687C16.2216 21.3924 16.3382 21.6609 16.3414 21.9741C16.3382 22.185 16.2823 22.3784 16.1737 22.5542C16.0682 22.7267 15.9292 22.8658 15.7566 22.9712C15.584 23.0735 15.3954 23.1246 15.1909 23.1246Z" fill="white"/>
        </svg>
      </div>
      <p className="explanatory-warning-text">{text}</p>
      <button 
        type="button"
        className="topic-submit-btn"
        onClick={closeModal}>
          I understand 
      </button>
    </Modal>
  );
};

export default ModalWarning;
  