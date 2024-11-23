
import { useState } from 'react';

function App() {
  const [query, setQuery] = useState('');
  const [movies, setMovies] = useState([]);
  const [error, setError] = useState(null);
  const [searchType, setSearchType] = useState('keyword'); 

  const handleSearch = async () => {
    if (!query) {
      setError("Search query cannot be empty.");
      return;
    }
    setError(null);

    console.log(`Searching for "${query}" using ${searchType} search`);

    try {
      const response = await fetch(
        searchType === 'keyword'
          ? `/search?query=${encodeURIComponent(query)}`
          : `/semantic-search?query=${encodeURIComponent(query)}` 
      );
      console.log("Response status:", response.status);

      if (response.status === 200) {
        const data = await response.json();
        console.log("Movies data:", data); 
        setMovies(data);
      } else {
        const errorData = await response.json();
        console.error("Error from server:", errorData);
        setError(errorData.error || "An unknown error occurred.");
      }
    } catch (e) {
      console.error("Fetch error:", e);
      setError("Failed to fetch data. Please check the server.");
    }
  };

  return (
    <div className="App">
      <h1>Movie Search</h1>

      {/* Search type selection */}
      <div>
        <button
          onClick={() => {
            setSearchType('keyword');
            setQuery(''); 
            setMovies([]); 
            setError(null); 
          }}
          style={{
            backgroundColor: searchType === 'keyword' ? '#4CAF50' : '#f0f0f0',
            color: searchType === 'keyword' ? 'white' : 'black',
            margin: '5px',
            padding: '10px',
          }}
        >
          Keyword Search
        </button>
        <button
          onClick={() => {
            setSearchType('semantic');
            setQuery('');
            setMovies([]);
            setError(null);
          }}
          style={{
            backgroundColor: searchType === 'semantic' ? '#4CAF50' : '#f0f0f0',
            color: searchType === 'semantic' ? 'white' : 'black',
            margin: '5px',
            padding: '10px',
          }}
        >
          Semantic Search
        </button>
      </div>

      {/* Render search view based on selected search type */}
      <div>
        <h2>{searchType === 'keyword' ? 'Keyword Search' : 'Semantic Search'}</h2>
        <input
          type="text"
          placeholder={`Enter a movie title for ${searchType} search`}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button onClick={handleSearch}>Search</button>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <ul>
          {movies.map((movie) => (
            <li key={movie.id}>{movie.title}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
