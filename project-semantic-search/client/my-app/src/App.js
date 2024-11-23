
import { useState } from 'react';

function App() {
  const [query, setQuery] = useState('');
  const [movies, setMovies] = useState([]);
  const [error, setError] = useState(null);

  const handleSearch = async () => {
    if (!query) {
      setError("Search query cannot be empty.");
      return;
    }
    setError(null);
  
    console.log("Searching for:", query); // Debug log
  
    try {
      const response = await fetch(`/search?query=${encodeURIComponent(query)}`);
      console.log("Response status:", response.status);
  
      if (response.status === 200) {
        const data = await response.json();
        console.log("Movies data:", data); // Debug log
        setMovies(data);
      } else {
        const errorData = await response.json();
        console.error("Error from server:", errorData); // Debug log
        setError(errorData.error || "An unknown error occurred.");
      }
    } catch (e) {
      console.error("Fetch error:", e); // Debug log
      setError("Failed to fetch data. Please check the server.");
    }
  };
  

  return (
    <div className="App">
      <h1>Movie Search</h1>
      <input
        type="text"
        placeholder="Search for a movie title"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button onClick={handleSearch}>Search</button>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <ul>
        {movies.map((movie) => (
          <li key={movie.id}>{movie.title}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;

