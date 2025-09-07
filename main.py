def iron_lady_chatbot():
    faq = {
        "1": {
            "question": "What programs does Iron Lady offer?",
            "answer": "Iron Lady offers leadership development programs focused on empowering women in business, entrepreneurship, and personal growth.",
            "keywords": ["programs", "offer", "courses", "leadership programs"]
        },
        "2": {
            "question": "What is the program duration?",
            "answer": "The program duration varies by course but typically ranges from 4 to 12 weeks.",
            "keywords": ["duration", "length", "time", "how long"]
        },
        "3": {
            "question": "Is the program online or offline?",
            "answer": "Iron Lady's leadership programs are offered both online and offline to accommodate different needs.",
            "keywords": ["online", "offline", "mode", "format", "in-person"]
        },
        "4": {
            "question": "Are certificates provided?",
            "answer": "Yes, certificates of completion are provided to participants who successfully finish the programs.",
            "keywords": ["certificate", "certification", "proof", "documents"]
        },
        "5": {
            "question": "Who are the mentors or coaches?",
            "answer": "The mentors and coaches are experienced leaders and industry experts committed to women’s leadership development.",
            "keywords": ["mentors", "coaches", "trainers", "instructors"]
        }
    }

    print("Welcome to the Iron Lady Leadership Program FAQ Chatbot.")
    print("Please choose a question by entering the corresponding number, or type your query keywords, or type 'exit' to quit.\n")

    # Display numbered questions
    for num, info in faq.items():
        print(f"{num}. {info['question']}")

    while True:
        user_input = input("\nEnter question number, keywords, or 'exit': ").strip().lower()
        if user_input == "exit":
            print("Thank you for visiting Iron Lady FAQ Bot. Goodbye!")
            break

        # Check if input matches a question number directly
        if user_input in faq:
            print("Chatbot:", faq[user_input]["answer"])
            continue

        # Otherwise, try to match keywords in user input to questions
        matched_answer = None
        for num, info in faq.items():
            if any(keyword in user_input for keyword in info["keywords"]):
                matched_answer = info["answer"]
                break

        if matched_answer:
            print("Chatbot:", matched_answer)
        else:
            print("Chatbot: Sorry, I didn't understand that. Please enter a valid question number, keywords related to the FAQ, or 'exit'.")

if __name__ == "__main__":
    iron_lady_chatbot()
