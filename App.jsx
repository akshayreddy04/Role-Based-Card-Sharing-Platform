import { Container, Stack, Text } from "@chakra-ui/react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import UserGrid from "./components/UserGrid";
import Login from "./components/login";
import { useState } from "react";

// Define BASE_URL for API calls
export const BASE_URL = import.meta.env.MODE === "development" ? "http://127.0.0.1:5000/api" : "/api";

function App() {
	const [users, setUsers] = useState([]);

	return (
		<Router>
			<Stack minH={"100vh"}>
				<Navbar setUsers={setUsers} />

				<Container maxW={"1200px"} my={4}>
					<Text
						fontSize={{ base: "3xl", md: "50" }}
						fontWeight={"bold"}
						letterSpacing={"2px"}
						textTransform={"uppercase"}
						textAlign={"center"}
						mb={8}
					>
						<Text as={"span"} bgGradient={"linear(to-r, cyan.400, blue.500)"} bgClip={"text"}>
							Let me know
						</Text>
						🚀
					</Text>

					{/* Define Routes */}
					<Routes>
						<Route path="/" element={<Login />} />
						<Route path="/users" element={<UserGrid users={users} setUsers={setUsers} />} />
					</Routes>
				</Container>
			</Stack>
		</Router>
	);
}

export default App;
