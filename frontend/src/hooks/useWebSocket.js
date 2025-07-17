import { useState, useEffect, useRef } from 'react';

export const useWebSocket = (url) => {
  const [connectionStatus, setConnectionStatus] = useState('Connecting');
  const [lastMessage, setLastMessage] = useState(null);
  const ws = useRef(null);

  useEffect(() => {
    const connect = () => {
      ws.current = new WebSocket(url);
      
      ws.current.onopen = () => {
        setConnectionStatus('Connected');
        console.log('WebSocket connected');
      };
      
      ws.current.onmessage = (event) => {
        setLastMessage(event);
      };
      
      ws.current.onclose = () => {
        setConnectionStatus('Disconnected');
        console.log('WebSocket disconnected');
        
        // Attempt to reconnect after 3 seconds
        setTimeout(() => {
          if (ws.current?.readyState === WebSocket.CLOSED) {
            connect();
          }
        }, 3000);
      };
      
      ws.current.onerror = (error) => {
        console.error('WebSocket error:', error);
        setConnectionStatus('Error');
      };
    };

    connect();

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [url]);

  return { lastMessage, connectionStatus };
};