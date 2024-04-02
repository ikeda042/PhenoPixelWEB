
import './App.css';
import Nav from './components/Nav';
import { Box } from '@mui/system';
import SquareImage from './components/Squareimage';
import DBtable from './components/Dbtable';
import Dbcontents from './pages/Ddcontents';
import Grid from '@mui/material/Unstable_Grid2';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';  // Import Routes
import React, { useEffect, useState } from 'react';
import Cell from './pages/Cell'
import DbcontentsOverview from './pages/Cellsoverview';
import { settings } from './settings';

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch(`${settings.url_prefix}/cellapi/cells/databases`)
      .then(response => response.json())
      .then(data => setData(data));
  }, []);

  return (
    <Router>
      <Box sx={{ bgcolor: "#f7f6f5", color: 'black', minHeight: '100vh' }}>
        <Nav />
        <Routes>

          <Route path="/" element={
            <>
              {/* <Link href="dbcontents">
                DbContents
              </Link> */}
              <Grid container spacing={4} margin={5}>
                <DBtable data={data} />
              </Grid >
            </>
          } />

          <Route path="/dbcontents/:filename" element={<Dbcontents />} />
          <Route path="/dbcontents/:filename/cell/:cellId" element={<Cell />} />
          <Route path="/dbcontents/:filename/overview" element={<DbcontentsOverview />} />
        </Routes>
      </Box >
    </Router>
  );
}

export default App;
