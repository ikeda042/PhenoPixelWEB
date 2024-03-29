import './App.css';
import Nav from './components/Nav';
import { Box } from '@mui/system';
import SquareImage
  from './components/Squareimage';
function App() {
  return (
    <>
      <Box sx={{ bgcolor: "#f7f6f5", color: 'black', minHeight: '100vh' }}>
        <Nav />
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
          <SquareImage imgSrc="testimg.png" size={400} />
        </Box>
      </Box >
    </>
  );
}

export default App;
