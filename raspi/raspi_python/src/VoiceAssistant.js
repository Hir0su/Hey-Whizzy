import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import idleGif from './idle.gif';
import talkingGif from './talking.gif';
import backgroundImage from './background.png';

const socket = io('http://localhost:5000');

const VoiceAssistant = () => {
  const [reply, setReply] = useState('');
  const [isTalking, setIsTalking] = useState(false);

  useEffect(() => {
    socket.on('reply', (reply) => {
      handleReply(reply);
    });
  }, []);

  const handleReply = (reply) => {
    setIsTalking(true);
    setReply(reply);
    setTimeout(() => {
      setIsTalking(false);
    }, 2000); // Change the delay as needed
  };

  return (
    <div
      style={{
        backgroundImage: `url(${backgroundImage})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        height: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <img src={isTalking ? talkingGif : idleGif} alt="Assistant" />
      <textarea
        value={reply}
        readOnly
        style={{
          width: '80%',
          height: '200px',
          fontSize: '1.2rem',
          padding: '10px',
          marginTop: '20px',
        }}
      />
    </div>
  );
};

export default VoiceAssistant;