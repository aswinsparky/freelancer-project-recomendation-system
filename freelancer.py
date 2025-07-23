import pandas as pd

user_data = {
    "First name": [],
    "Last name": [],
    "User name": [],
    "Profession": [],
    "Email": [],
    "Password": [],
    "Skillset": []
}

project_data = {
    "User name": [],
    "Project title": [],
    "Required skillset": [],
    "Expected duration": [],
    "Project description": []
}

df = pd.DataFrame(user_data)
project_df = pd.DataFrame(project_data)

# Load CSV files if exist
try:
    df = pd.read_csv("freelancer_user_data.csv")
except FileNotFoundError:
    df.to_csv("freelancer_user_data.csv", index=False)

try:
    project_df = pd.read_csv("project_data.csv")
except FileNotFoundError:
    project_df.to_csv("project_data.csv", index=False)

status_account = input("Type 'login' to login or 'register' to create an account: ").lower()

if status_account == "register":
    first_name = input("Enter your First name: ")
    last_name = input("Enter your Last name: ")
    user_name = input("Enter a unique User name: ")
    profession = input("Enter your profession (freelancer/employer): ").lower()
    email = input("Enter your email ID: ")
    password = input("Create a password: ")
    skillset = input("Enter your skillset (comma-separated): ")

    new_user = pd.DataFrame({
        "First name": [first_name],
        "Last name": [last_name],
        "User name": [user_name],
        "Profession": [profession],
        "Email": [email],
        "Password": [password],
        "Skillset": [skillset]
    })

    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv("freelancer_user_data.csv", index=False)
    print("Registration successful.")

elif status_account == "login":
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    user = df[(df["User name"] == username) & (df["Password"] == password)]

    if user.empty:
        raise Exception("Invalid username or password")

    profession = user.iloc[0]["Profession"]
    print(f"Welcome back, {username}! You are logged in as a {profession}.")

    if profession == "employer":
        action = input("Type 'upload' to upload project, 'recommend' to get freelancer recommendations, or 'view' to view all projects: ").strip().lower()

        if action == "upload":
            project_title = input("Enter the project title: ")
            required_skills = input("Enter required skillset (comma-separated): ")
            duration = input("Enter expected duration: ")
            description = input("Enter project description: ")

            new_project = pd.DataFrame({
                "User name": [username],
                "Project title": [project_title],
                "Required skillset": [required_skills],
                "Expected duration": [duration],
                "Project description": [description]
            })

            project_df = pd.concat([project_df, new_project], ignore_index=True)
            project_df.to_csv("project_data.csv", index=False)
            print("✅ Project uploaded successfully!")

        elif action == "recommend":
            if project_df.empty:
                print("⚠️ No projects available.")
            else:
                title = input("Enter the project title to find freelancers for: ")
                project = project_df[(project_df["Project title"] == title) & (project_df["User name"] == username)]

                if project.empty:
                    print("❌ No such project found under your username.")
                else:
                    skills_needed = project.iloc[0]["Required skillset"].lower().split(",")
                    matched_freelancers = df[df["Profession"] == "freelancer"].copy()
                    matched_freelancers["Match Score"] = matched_freelancers["Skillset"].apply(
                        lambda s: len(set(s.lower().split(",")) & set(skills_needed))
                    )
                    matched_freelancers = matched_freelancers[matched_freelancers["Match Score"] > 0]
                    matched_freelancers = matched_freelancers.sort_values(by="Match Score", ascending=False)

                    if matched_freelancers.empty:
                        print("❌ No matching freelancers found.")
                    else:
                        print("🎯 Recommended Freelancers:")
                        print(matched_freelancers[["First name", "Last name", "User name", "Email", "Skillset", "Match Score"]])

        elif action == "view":
            if not project_df.empty:
                print("\n📋 All Available Projects:")
                print(project_df[["Project title", "Required skillset", "Expected duration", "Project description"]])
            else:
                print("⚠️ No projects found.")

    elif profession == "freelancer":
        skills = user.iloc[0]["Skillset"].lower().split(",")

        matching_projects = project_df[project_df["Required skillset"].apply(
            lambda s: len(set(s.lower().split(",")) & set(skills)) > 0)]

        if matching_projects.empty:
            print("❌ No matching projects found.")
        else:
            print("🎯 Recommended Projects:")
            print(matching_projects[["Project title", "Required skillset", "Expected duration", "Project description"]])

        action = input("Type 'update' to update skillset or 'view' to view all projects: ").strip().lower()

        if action == "update":
            new_skills = input("Enter your new skillset (comma-separated): ")
            df.loc[df["User name"] == username, "Skillset"] = new_skills
            df.to_csv("freelancer_user_data.csv", index=False)
            print("✅ Skillset updated successfully.")

        elif action == "view":
            if not project_df.empty:
                print("\n📋 All Available Projects:")
                print(project_df[["Project title", "Required skillset", "Expected duration", "Project description"]])
            else:
                print("⚠️ No projects found.")

else:
    print("Invalid input. Please type 'login' or 'register'.")
