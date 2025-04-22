import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Landing from './pages/Landing';
import MusicRecommend from './pages/MusicRecommend';
import Layout from './components/Layout';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Landing />} />
          <Route path="/musicrecommend" element={<MusicRecommend />} />
          {/* Future routes will be added here */}
          <Route path="*" element={<div className="h-screen flex items-center justify-center">Page not found</div>} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;