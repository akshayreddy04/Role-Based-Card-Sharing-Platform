import { useState } from "react";
import {
  Box,
  Button,
  Container,
  Flex,
  FormControl,
  FormLabel,
  Heading,
  Input,
  Text,
  Link,
  VStack,
  useColorModeValue,
  useToast,
  Spinner,
} from "@chakra-ui/react";
import { motion } from "framer-motion";
import axios from "axios";
import { useNavigate } from "react-router-dom"; // Import useNavigate

export default function LoginSignup() {
  const [isLogin, setIsLogin] = useState(true);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({ name: "", email: "", password: "" });
  const toast = useToast();
  const navigate = useNavigate(); // Initialize useNavigate

  const bgColor = useColorModeValue("white", "gray.800");
  const inputBg = useColorModeValue("gray.100", "gray.700");

  const API_BASE_URL = "http://localhost:5000/api/friends"; // Adjust to your backend URL

  // Handle input change
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Handle login/signup request
  const handleSubmit = async () => {
    setLoading(true);
    
    try {
      if (isLogin) {
        // Login API Call
        const response = await axios.post(`${API_BASE_URL}/login`, {
          email: formData.email,
          password: formData.password,
        });

        if (response.data.status === "success") {
          toast({
            title: "Login Successful",
            description: response.data.message,
            status: "success",
            duration: 3000,
            isClosable: true,
          });

          // Redirect to /user after successful login
          navigate("/users", { state: { useremail: formData.email } });
          
        } else {
          toast({
            title: "Login Failed",
            description: "Invalid credentials. Please try again.",
            status: "error",
            duration: 3000,
            isClosable: true,
          });
        }
      } else {
        // Signup API Call
        const response = await axios.post(`${API_BASE_URL}/signup`, {
          name: formData.name,
          email: formData.email,
          password: formData.password,
        });

        if (response.status === 200) {
          toast({
            title: "Signup Successful",
            description: "Your account has been created!",
            status: "success",
            duration: 3000,
            isClosable: true,
          });
          setIsLogin(true); // Switch to login after signup
        }
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Something went wrong. Please try again.",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Flex minH="100vh" align="center" justify="center" bgGradient="linear(to-r, blue.400, purple.500)">
      <Container maxW="md" p={6} bg={bgColor} borderRadius="lg" boxShadow="xl">
        <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
          <Heading textAlign="center" mb={4} color="blue.500">
            {isLogin ? "Login" : "Sign Up"}
          </Heading>

          <VStack spacing={4}>
            {!isLogin && (
              <FormControl>
                <FormLabel>Name</FormLabel>
                <Input name="name" placeholder="John Doe" bg={inputBg} onChange={handleChange} />
              </FormControl>
            )}

            <FormControl>
              <FormLabel>Email</FormLabel>
              <Input name="email" type="email" placeholder="you@example.com" bg={inputBg} onChange={handleChange} />
            </FormControl>

            <FormControl>
              <FormLabel>Password</FormLabel>
              <Input name="password" type="password" placeholder="********" bg={inputBg} onChange={handleChange} />
            </FormControl>

            <Button colorScheme="blue" w="full" onClick={handleSubmit} isDisabled={loading}>
              {loading ? <Spinner size="sm" /> : isLogin ? "Login" : "Sign Up"}
            </Button>

            <Text>
              {isLogin ? "Don't have an account?" : "Already have an account?"}{" "}
              <Link color="blue.400" cursor="pointer" onClick={() => setIsLogin(!isLogin)}>
                {isLogin ? "Sign Up" : "Login"}
              </Link>
            </Text>
          </VStack>
        </motion.div>
      </Container>
    </Flex>
  );
}
