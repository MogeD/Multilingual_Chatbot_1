import React, { useState, useEffect, useRef } from 'react';
import {
  Container,
  Paper,
  TextField,
  Button,
  Box,
  Typography,
  Select,
  MenuItem,
  AppBar,
  Toolbar,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import LanguageIcon from '@mui/icons-material/Language';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

// Add language display names mapping
const LANGUAGE_NAMES = {
  // Indian Languages
  'hi': 'Hindi',
  'te': 'Telugu',
  'ta': 'Tamil',
  'kn': 'Kannada',
  'ml': 'Malayalam',
  'bn': 'Bengali',
  'gu': 'Gujarati',
  
  // Nigerian Languages
  'yo': 'Yoruba',
  'ha': 'Hausa',
  'ig': 'Igbo',
  
  // Other African Languages
  'sw': 'Swahili',
  'am': 'Amharic',
  
  // European Languages
  'fr': 'French',
  'es': 'Spanish',
  
  // East Asian Languages
  'zh': 'Chinese',
  'ja': 'Japanese',
  'ko': 'Korean'
};

function App() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('hi');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!inputMessage.trim()) return;

    const newMessage = {
      text: inputMessage,
      sender: 'user',
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, newMessage]);
    setInputMessage('');

    try {
      const response = await axios.post(`${API_URL}/chat`, {
        message: inputMessage,
        language: selectedLanguage,
      });

      const botMessage = {
        text: response.data.response,
        sender: 'bot',
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <LanguageIcon sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Regional Language Chatbot
          </Typography>
          <Select
            value={selectedLanguage}
            onChange={(e) => setSelectedLanguage(e.target.value)}
            sx={{ 
              color: 'white', 
              '& .MuiSelect-icon': { color: 'white' },
              minWidth: '150px'
            }}
          >
            <MenuItem disabled style={{ opacity: 0.7 }}>Indian Languages</MenuItem>
            <MenuItem value="hi">Hindi</MenuItem>
            <MenuItem value="te">Telugu</MenuItem>
            <MenuItem value="ta">Tamil</MenuItem>
            <MenuItem value="kn">Kannada</MenuItem>
            <MenuItem value="ml">Malayalam</MenuItem>
            <MenuItem value="bn">Bengali</MenuItem>
            <MenuItem value="gu">Gujarati</MenuItem>
            
            <MenuItem disabled style={{ opacity: 0.7 }}>Nigerian Languages</MenuItem>
            <MenuItem value="yo">Yoruba</MenuItem>
            <MenuItem value="ha">Hausa</MenuItem>
            <MenuItem value="ig">Igbo</MenuItem>
            
            <MenuItem disabled style={{ opacity: 0.7 }}>Other African Languages</MenuItem>
            <MenuItem value="sw">Swahili</MenuItem>
            <MenuItem value="am">Amharic</MenuItem>
            
            <MenuItem disabled style={{ opacity: 0.7 }}>European Languages</MenuItem>
            <MenuItem value="fr">French</MenuItem>
            <MenuItem value="es">Spanish</MenuItem>
            
            <MenuItem disabled style={{ opacity: 0.7 }}>East Asian Languages</MenuItem>
            <MenuItem value="zh">Chinese</MenuItem>
            <MenuItem value="ja">Japanese</MenuItem>
            <MenuItem value="ko">Korean</MenuItem>
          </Select>
        </Toolbar>
      </AppBar>

      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Paper 
          elevation={3} 
          sx={{ 
            height: '70vh', 
            display: 'flex', 
            flexDirection: 'column',
            bgcolor: '#1a1a1a'
          }}
        >
          <Box 
            sx={{ 
              flex: 1, 
              overflow: 'auto', 
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              gap: 1
            }}
          >
            {messages.map((message, index) => (
              <Box
                key={index}
                sx={{
                  display: 'flex',
                  justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start',
                }}
              >
                <Paper
                  sx={{
                    p: 1,
                    maxWidth: '70%',
                    bgcolor: message.sender === 'user' ? '#2979ff' : '#424242',
                    color: 'white',
                    borderRadius: 2,
                  }}
                >
                  <Typography>{message.text}</Typography>
                </Paper>
              </Box>
            ))}
            <div ref={messagesEndRef} />
          </Box>

          <Box sx={{ p: 2, bgcolor: '#424242' }}>
            <Box sx={{ display: 'flex', gap: 1 }}>
              <TextField
                fullWidth
                variant="outlined"
                placeholder={`Type your message in ${LANGUAGE_NAMES[selectedLanguage]}...`}
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    color: 'white',
                    '& fieldset': {
                      borderColor: 'rgba(255, 255, 255, 0.23)',
                    },
                    '&:hover fieldset': {
                      borderColor: 'rgba(255, 255, 255, 0.23)',
                    },
                    '&.Mui-focused fieldset': {
                      borderColor: '#2979ff',
                    },
                  },
                }}
              />
              <Button
                variant="contained"
                color="primary"
                endIcon={<SendIcon />}
                onClick={handleSend}
              >
                Send
              </Button>
            </Box>
          </Box>
        </Paper>
      </Container>
    </Box>
  );
}

export default App; 