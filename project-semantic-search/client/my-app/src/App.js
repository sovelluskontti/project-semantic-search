

import { useState, useEffect } from "react";

function App() {
  const [query, setQuery] = useState("");
  const [movies, setMovies] = useState(null);
  const [error, setError] = useState(null);
  const [searchType, setSearchType] = useState("keyword");

  const [category, setCategory] = useState("");
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [productSearch, setProductSearch] = useState("");
  const [inStock, setInStock] = useState(false);
  const [resultsCount, setResultsCount] = useState(null);
  const [categoryCounts, setCategoryCounts] = useState({}); 


  const handleSearch = async () => {
    setError(null);
    setMovies(null);
    setResultsCount(null);
    setCategoryCounts({});
    console.log(`Searching using ${searchType} search`);

    try {
      let response;
      if (searchType === "keyword" || searchType === "semantic") {
        if (!query) {
          setError("Search query cannot be empty.");
          return;
        }
        response = await fetch(
          searchType === "keyword"
            ? `/search?query=${encodeURIComponent(query)}`
            : `/semantic-search?query=${encodeURIComponent(query)}`
        );
      } else if (searchType === "faceted") {
        const params = new URLSearchParams();
        if (category) params.append("category", category);
        if (minPrice) params.append("min_price", minPrice);
        if (maxPrice) params.append("max_price", maxPrice);
        if (productSearch) params.append("name", productSearch);
        if (inStock) params.append("in_stock", "1");
        response = await fetch(`/faceted-search?${params.toString()}`);
      }

      console.log("Response status:", response.status);

      if (response.ok) {
        const data = await response.json();
        console.log("Search results:", data);
        if (searchType === "keyword" || searchType === "semantic") {
          setMovies(data); 
        } else if (searchType === "faceted") {
          setMovies(data.products); 
          setResultsCount(data.total_count); 
          setCategoryCounts(data.category_counts || {}); 
        }
      } else {
        const errorData = await response.json();
        console.error("Server error:", errorData);
        setError(errorData.error || "An unknown error occurred.");
      }
    } catch (e) {
      console.error("Fetch error:", e);
      setError("Failed to fetch data. Please check the server.");
    }
  };

  useEffect(() => {
    if (searchType === "faceted") {
      handleSearch();
    }
  }, [searchType]);

  const resetState = (type) => {
    setSearchType(type);
    setMovies(null);
    setError(null);
    setQuery("");
    setCategory("");
    setMinPrice("");
    setMaxPrice("");
    setProductSearch("");
  };

  return (
    <div className="App" style={{ display: "flex", flexDirection: "column", height: "100vh" }}>
      <h1 style={{ textAlign: "center", marginTop: "20px" }}>Product & Movie Search</h1>

      {/* Search Type Buttons */}
      <div style={{ textAlign: "center", marginBottom: "20px" }}>
        {["keyword", "semantic", "faceted"].map((type) => (
          <button
            key={type}
            onClick={() => resetState(type)}
            style={{
              backgroundColor: searchType === type ? "#4CAF50" : "#f0f0f0",
              color: searchType === type ? "white" : "black",
              margin: "5px",
              padding: "10px",
              border: "none",
              cursor: "pointer",
            }}
          >
            {type.charAt(0).toUpperCase() + type.slice(1)} Search
          </button>
        ))}
      </div>

      {/* Main content area */}
      <div style={{ display: "flex", flex: 1 }}>
        {/* Sidebar Filters */}
        {searchType === "faceted" && (
          <div
            style={{
              width: "25%",
              backgroundColor: "#f8f8f8",
              padding: "20px",
              boxShadow: "2px 0 5px rgba(0,0,0,0.1)",
            }}
          >
          <h2 style={{ textAlign: "center" }}>Faceted Filters</h2>

            <div style={{ marginBottom: "20px" }}>
              <h3>Category</h3>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  padding: "10px 0",
                }}
              >
                <button
                  onClick={() =>
                    setCategory(category === "Power Tools" ? "" : "Power Tools")
                  }                  
                  style={{
                    padding: "10px",
                    backgroundColor: category === "Power Tools" ? "#008CBA" : "#f8f8f8",
                    color: category === "Power Tools" ? "white" : "black",
                    border: "1px solid #ccc",
                    borderRadius: "5px",
                    width: "48%",
                    cursor: "pointer",
                  }}
                >
                  Power Tools ({categoryCounts?.["Power Tools"] || 0})
                </button>
                <button
                  onClick={() =>
                    setCategory(category === "Drilling Tools" ? "" : "Drilling Tools")
                  }                  
                  style={{
                    padding: "10px",
                    backgroundColor: category === "Drilling Tools" ? "#008CBA" : "#f8f8f8",
                    color: category === "Drilling Tools" ? "white" : "black",
                    border: "1px solid #ccc",
                    borderRadius: "5px",
                    width: "48%",
                    cursor: "pointer",
                  }}
                >
                  Drilling Tools ({categoryCounts?.["Drilling Tools"] || 0})
                </button>
              </div>
            </div>

            {/* Price Range Slider */}
            <div>
            <h3>Price</h3>
              <label style={{ display: "block", textAlign: "center", marginBottom: "10px" }}>
                {`Price Range: ${minPrice}€ - ${maxPrice}€`}
              </label>

              <input
                type="range"
                min="0"
                max="200"
                value={minPrice}
                onChange={(e) => setMinPrice(e.target.value)}
                style={{
                  width: "100%",
                  marginBottom: "10px",
                }}
              />

              <input
                type="range"
                min={minPrice} 
                max="200"
                value={maxPrice}
                onChange={(e) => setMaxPrice(e.target.value)}
                style={{
                  width: "100%",
                  marginBottom: "10px",
                }}
              />
            </div>

            {/* In Stock Filter */}
            <div style={{ marginTop: "20px" }}>
              <h3>Availability</h3>
              <label style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                <input
                  type="checkbox"
                  checked={inStock}
                  onChange={() => setInStock(!inStock)}
                />
                In Stock
              </label>
            </div>


            <button
              onClick={handleSearch}
              style={{
                padding: "10px",
                backgroundColor: "#008CBA",
                color: "white",
                border: "none",
                width: "100%",
                cursor: "pointer",
                borderRadius: "5px",
              }}
            >
              Apply Filters
            </button>
          </div>
        )}

        {/* Main Product/Movie Display */}
        <div
          style={{
            flex: 1,
            padding: "20px",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          {/* Product Name Search Bar for Faceted Search */}
          {searchType === "faceted" && (
            <div style={{ marginBottom: "20px", display: "flex", alignItems: "center" }}>
              <input
                type="text"
                placeholder="Search product name"
                value={productSearch}
                onChange={(e) => setProductSearch(e.target.value)}
                style={{
                  padding: "10px",
                  marginRight: "10px",
                  width: "400px",
                  border: "1px solid #ccc",
                  borderRadius: "5px",
                }}
              />
              <button
                onClick={handleSearch}
                style={{
                  padding: "10px",
                  backgroundColor: "#008CBA",
                  color: "white",
                  border: "none",
                  cursor: "pointer",
                  borderRadius: "5px",
                }}
              >
                Search
              </button>
            </div>
          )}

          {/* Display Results Count */}
          {resultsCount !== null && searchType === "faceted" && (
            <div style={{ marginBottom: "20px", textAlign: "center" }}>
              <p><strong>Total Results: {resultsCount}</strong></p>
            </div>
          )}

          {/* Keyword / Semantic search input */}
          {(searchType === "keyword" || searchType === "semantic") && (
            <div style={{ marginBottom: "20px" }}>
              <input
                type="text"
                placeholder={`Enter a movie title for ${searchType} search`}
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                style={{
                  padding: "10px",
                  marginRight: "10px",
                  width: "300px",
                  border: "1px solid #ccc",
                  borderRadius: "5px",
                }}
              />
              <button
                onClick={handleSearch}
                style={{
                  padding: "10px",
                  backgroundColor: "#008CBA",
                  color: "white",
                  border: "none",
                  cursor: "pointer",
                  borderRadius: "5px",
                }}
              >
                Search
              </button>
            </div>
          )}

          {/* Error */}
          {error && <p style={{ color: "red", marginTop: "10px" }}>{error}</p>}

          {/* Results */}
          <div style={{ width: "80%", marginTop: "20px" }}>
            {movies === null ? null : movies.length > 0 ? (
              movies.map((item, index) => (
                <div
                  key={index}
                  style={{
                    margin: "10px 0",
                    padding: "10px 20px",
                    backgroundColor: "#f9f9f9",
                    borderRadius: "5px",
                    boxShadow: "0px 0px 5px rgba(0,0,0,0.1)",
                    textAlign: "center",
                  }}
                >
                  {searchType === "faceted" ? (
                    <div>
                      <p><strong>Name:</strong> {item.name}</p>
                      <p><strong>Category:</strong> {item.category}</p>
                      <p><strong>Manufacturer:</strong> {item.manufacturer}</p>
                      <p><strong>Price:</strong> ${item.price.toFixed(2)}</p>
                      <p><strong>Stock:</strong> {item.stock > 0 ? item.stock : "Out of stock"}</p>
                      <p><strong>Description:</strong> {item.description}</p>
                    </div>
                  ) : (
                    <div>{item.title}</div>
                  )}

                </div>
              ))
            ) : (
              <p style={{ textAlign: "center", marginTop: "20px" }}>
                No results found. Try a different search.
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
