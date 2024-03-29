import React from 'react';
import './App.css';
import Nav from './components/Nav';
import { Box } from '@mui/system';
import SquareImage from './components/Squareimage';
import DBtable from './components/Dbtable';
import Dbcontents from './pages/Ddcontents';
import Grid from '@mui/material/Unstable_Grid2';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';  // Import Routes
import { Link } from 'react-router-dom';

function App() {
  return (
    <Router>
      <Box sx={{ bgcolor: "#f7f6f5", color: 'black', minHeight: '100vh' }}>
        <Nav />
        <Routes>

          <Route path="/" element={
            <>
              <Link to="/dbcontents">DbContents</Link>
              <Grid container spacing={4} margin={5}>
                <DBtable />
              </Grid >
              <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
                <SquareImage imgSrc="testimg.png" size={400} />
              </Box>
            </>
          } />

          <Route path="/dbcontents" element={<Dbcontents />} />
        </Routes>
      </Box >
    </Router>
  );
}

export default App;
