import React, { useState, useEffect, useRef } from 'react';
import io from 'socket.io-client';
import idleGif from './idle.gif';
import talkingGif from './talking.gif';
import './VoiceAssistant.css';
import './Montserrat-Regular.ttf';
import './Montserrat-Bold.ttf';
import './Montserrat-SemiBold.ttf';
import './Montserrat-ExtraBold.ttf';
import './Montserrat-Medium.ttf';

const socket = io('http://localhost:5000');

const VoiceAssistant = () => {
  const [reply, setReply] = useState('');
  const [isTalking, setIsTalking] = useState(false);
  const [backgroundIndex, setBackgroundIndex] = useState(1);
  const [imageData, setImageData] = useState(null);

  const labelRef = useRef(null);
  const defaultFontSize = 60; // Default font size

  useEffect(() => {
    socket.on('reply', (reply) => {
      handleReply(reply);
    });

    socket.on('reply_large', (reply) => {
      handleReplyLarge(reply);
    });

    socket.on('stop_talking', () => {
      stopTalking();
    });

    socket.on('idle', () => {
      idle();
    });

    socket.on('idle_stop', () => {
      idle_stop();
    });

    socket.on('change_background', (index) => {
      handleBackgroundChange(index);
    });

    socket.on('image_data', (file_name) => {
      const imageUrl = `http://IP ADDRESS HERE/uploads/${file_name}`;
      setImageData(imageUrl);
    });

    const handleResize = () => {
      const labelContainer = labelRef.current;
      const containerWidth = labelContainer.offsetWidth;
      const containerHeight = 375; // Fixed height of 180px
      const text = labelContainer.querySelector('span');
      let fontSize = defaultFontSize;

      while (
        text.offsetWidth > containerWidth ||
        text.offsetHeight > containerHeight
      ) {
        fontSize -= 1;
        text.style.fontSize = `${fontSize}px`;
      }
    };

    window.addEventListener('resize', handleResize);
    handleResize(); // Call the function initially

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, [reply]);

  const handleReply = (reply) => {
    setIsTalking(true);
    setReply(reply);
  };

  const handleReplyLarge = (reply) => {
    setIsTalking(true);
    setReply(reply);
    const labelContainer = labelRef.current;
    labelContainer.style.height = '700px';
    labelContainer.style.top = '270px';
  };

  const stopTalking = () => {
    setIsTalking(false);
  };

  const idle = () => {    setIsTalking(false);
    setReply('Say "Hey Whizzy"');
    const labelContainer = labelRef.current;
    const text = labelContainer.querySelector('span');
    text.style.fontSize = `${defaultFontSize}px`; // Reset font size
    labelContainer.style.height = '375px'; // Reset height to default
    labelContainer.style.top = '850px';
    setImageData(null);
  };

  const idle_stop = () => {
    setIsTalking(false);
    setReply('');
  };

  const handleBackgroundChange = (index) => {
    setBackgroundIndex(index);
  };

  return (
    <div
      className="voice-assistant-container"
      style={{
        backgroundImage: `url(${require(`./bg${backgroundIndex}.png`)})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        height: '100vh',
        position: 'relative',
      }}
    >
      {imageData && (
        <div className="image-container">
          <img src={imageData} alt="Received" />
        </div>
      )}
      <div className="label-container" ref={labelRef}>
        <span>{reply}</span>
      </div>
      <div className="gif-container">
        <img src={isTalking ? talkingGif : idleGif} alt="Assistant" />
      </div>
    </div>
  );
};

export default VoiceAssistant;