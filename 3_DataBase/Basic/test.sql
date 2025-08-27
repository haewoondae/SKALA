CREATE TABLE models (
    model_id SERIAL PRIMARY KEY,
    model_name VARCHAR(50) UNIQUE NOT NULL
);


CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE prompt_responses (
    prompt_response_id SERIAL PRIMARY KEY,  
    prompt_text TEXT NOT NULL,             
    response_text TEXT NOT NULL           
);

CREATE TABLE feedback (
    feedback_id VARCHAR(10) PRIMARY KEY,       
    user_id INT NOT NULL,                       
    model_id INT NOT NULL,                      
    prompt_response_id INT NOT NULL,            
    rating NUMERIC(2,1) CHECK (rating >= 0 AND rating <= 5),
    
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (model_id) REFERENCES models(model_id),
    FOREIGN KEY (prompt_response_id) REFERENCES prompt_responses(prompt_response_id) 
);

CREATE TABLE feedback_tags (
    tag_id SERIAL PRIMARY KEY,
    feedback_id VARCHAR(10) NOT NULL,
    tag VARCHAR(50) NOT NULL,
    FOREIGN KEY (feedback_id) REFERENCES feedback(feedback_id) ON DELETE CASCADE
);
