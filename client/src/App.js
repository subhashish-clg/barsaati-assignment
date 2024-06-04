import { useState } from "react";
import axios from "axios";
import JsonView from "@uiw/react-json-view";

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [trends, setTrends] = useState(undefined);

  async function getTrends(url) {
    setIsLoading(true);
    setTrends(undefined);

    try {
      const data = await axios.get(url, {
        timeout: 300000,
      });

      setTrends(data.data);
      setIsLoading(false);
    } catch {
      alert("Failed to fetch data from the server.");
      setIsLoading(false);
    }
  }

  return (
    <main className="container mx-auto py-8 px-4">
      <div>
        <a
          className="text-blue-400 underline hover:text-blue-600 cursor-pointer"
          onClick={async (e) => {
            e.preventDefault();

            getTrends(
              `${process.env.REACT_APP_SERVER_URL}/trends?fallback=latest`
            );
          }}
        >
          Click here to run the script
        </a>
        <a
          className="ml-4 text-blue-400 underline hover:text-blue-600 cursor-pointer"
          onClick={async (e) => {
            e.preventDefault();
            console.log(process.env.REACT_APP_SERVER_URL);

            getTrends(
              `${process.env.REACT_APP_SERVER_URL}/trends?fallback=cache`
            );
          }}
        >
          (or retrieve from cache)
        </a>

        {isLoading && <p className="mt-8">Loading</p>}
        {trends && (
          <div className="space-y-8 pt-8">
            <p>These are the most happening topics as on {trends["date"]}.</p>

            <ul className="space-y-4">
              {trends["trends"].map((trend) => {
                return (
                  <li key={trend["hashtag"]} className="flex flex-col">
                    <span className="font-bold">#{trend["hashtag"]}</span>
                    <span className="ml-2">- {trend["trending_in"]}</span>
                    <span className="ml-2">
                      -{trend["additional_description"]}
                    </span>
                  </li>
                );
              })}
            </ul>

            <p>
              The IP Address used for this query is was
              <span className="font-bold text-gray-800 ml-2 underline">
                {trends["IP"]}
              </span>
            </p>

            <JsonView value={trends["trends"]} />
          </div>
        )}
      </div>
    </main>
  );
}

export default App;
