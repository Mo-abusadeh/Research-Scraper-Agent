import logging

class AbstractSummariser: 

    def __init__(self, api_key=None, model_path=None):
        """
        Initialise the class with an API key from Gemini

        Args: 
            api_key: (str)
            model_path: (str)
        
        """
        import os 
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY") # COMMENT OUT TO USE Llama 
        #self.api_key = api_key # UNCOMMENT TO USE Llama
        self.genai = None
        self.llm = None
        
        
        # Initialising the Gemini Client
        if self.api_key: 
            try:
                import google.generativeai as genai
                # Configure the API key
                genai.configure(api_key=self.api_key)
                self.genai = genai
                logging.info("Initialised Gemini API with key")

            except ImportError:
                logging.warning("Failed to import the Google Generative AI library, using the fallback local model instead (llama-2-7b-chat.Q4_K_M.gguf)")
        else:
            logging.warning("No API key was found, will use the fallback local model instead (llama-2-7b-chat.Q4_K_M.gguf)")
        
         # Initialising the llama-cpp-python model
        if not self.genai or model_path:
            try: 
                from llama_cpp import Llama
                
                if model_path:
                    # Use the provided model path
                    logging.info(f"Loading Llama model from {model_path}")
                    self.llm = Llama(model_path=model_path)
                else:
                    # Download a model if it doesn't exist
                    import huggingface_hub
                    
                    logging.info("Downloading Llama model from HuggingFace (this may take a few minutes)")
                    model_name = "llama-2-7b-chat.Q4_K_M.gguf"
                    model_path = f"models/{model_name}"
                    
                    # Check if model already exists
                    if not os.path.exists(model_path):
                        huggingface_hub.hf_hub_download(
                            repo_id="TheBloke/Llama-2-7B-Chat-GGUF",
                            filename=model_name,
                            local_dir=os.getcwd()
                        )
                    
                    logging.info(f"Initialising Llama model from {model_path}")
                    self.llm = Llama(model_path=model_path, n_ctx=2048, n_threads=4, n_gpu_layers=0)
                
                logging.info("Llama model initialised successfully")

            except ImportError: 
                logging.warning("llama-cpp-python is not installed please install it using pip")

            except Exception as e: 
                logging.warning(f"Llama model failed to be initialised, Error: {str(e)}")


    def summarise(self, text): 
        """
        Summarises the abstract content using either Google's Gemini model via API, 
            a small local Llama model or a simple extraction by taking the first two sentences.

        Args: 
            text: (str)
        
        Returns:
            Summarised Text: (str)
        
        """
        # Try to use the Gemini model first
        if self.genai: 
            try:
                logging.info("Attempting to use Gemini model for summarization")
                prompt = f"""The following is an academic abstract, please summarise it effectively and concisely into 3-4 sentences {text}"""
                
                # Use the generative model to create a response
                logging.info("Creating Gemini model instance")
                model = self.genai.GenerativeModel('gemini-2.0-flash-lite')
                
                logging.info("Sending prompt to Gemini API")
                response = model.generate_content(prompt)
                
                abstract_summary = response.text.strip()
                logging.info("Summary generated successfully using Gemini")
                return abstract_summary
            
            except Exception as e: 
                logging.error(f"The summary failed to generate using Gemini, Error: {str(e)}")
                import traceback
                logging.error(f"Traceback: {traceback.format_exc()}")

        # Use the local Llama model in the case where Llama had been initialised
        elif self.llm: 
            try:
                # Prompt formatted for the llama 2 chat
                prompt = f"<s>[INST] The following is an academic abstract, please summarise it effectively and concisely into 3-4 sentences \n\n{text} [/INST]"

                # Generate summary using Llama (output of max 100 tokens (around 75 words))
                output = self.llm(
                    prompt,
                    max_tokens=100,
                    stop=["</s>", "\n\n"],
                    echo=False
                )
                summary = output["choices"][0]["text"].strip()
                logging.info("Summary Generated Successfully using local Llama model")
                return summary
            
            except Exception as e: 
                logging.error(f"The summary failed to generate using Llama, Error: {str(e)}")

        # Simple Extraction (Last Fallback): just using the first 4 sentences from the Abstract if neither models work
        logging.info("Falling back to simple extraction method - neither Gemini nor Llama models were able to generate a summary")
        sentences = text.split(". ")
        if len(sentences) <= 4:
            return text
        return ". ".join(sentences[:4]) + "."
    

    def Summarise_abstracts(self, texts):
        """
        Collects all the parsed abstracts and calls the summarise method on each

        Args:
            texts: (list)
            
        Returns: 
            Summarised Abstracts: (List)
        
        """
        logging.info(f"Summarising {len(texts)} abstracts")

        summaries = []

        # Summarising the abstracts one by one
        for i, text in enumerate(texts): 
            logging.info(f"summarising abstract {i+1}/{len(texts)}")
            
            # Using the main summarise function
            try: 
                summary = self.summarise(text)
                summaries.append(summary)

            except Exception as e: 
                logging.error(f"Error summarising abstract {i+1}: {str(e)}")
                
                # Keep a placeholder if processing the summary function fails
                summaries.append("Summary unavailable (Error in summarising)")

        logging.info(f"successfully summarised {len(summaries)} abstracts")
        
        return summaries