import React from 'react';
import './App.css';
import Nav from './components/Nav';
import { Box } from '@mui/system';
import SquareImage from './components/Squareimage';
import DBtable from './components/Dbtable';
import Dbcontents from './pages/Ddcontents';
import Grid from '@mui/material/Unstable_Grid2';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';  // Import Routes
import Link from '@mui/material/Link';


function App() {
  const data = [
    {
      "file_name": "sk326tri120min.db",
      "cell_count": 54
    },

  ];
  return (
    <Router>
      <Box sx={{ bgcolor: "#f7f6f5", color: 'black', minHeight: '100vh' }}>
        <Nav />
        <Routes>

          <Route path="/" element={
            <>
              <Link href="dbcontents">
                DbContents
              </Link>
              <Grid container spacing={4} margin={5}>
                <DBtable data={data} />
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
