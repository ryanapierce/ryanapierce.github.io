# Use Node.js as the base image since Firebase CLI requires Node.js
FROM node:18

# Set working directory
WORKDIR /etl_pipeline_demo

# Install Firebase CLI globally
RUN npm install -g firebase-tools

# Copy Firebase configuration files into the container
COPY firebase/firebase.json ./
COPY firebase/.firebaserc ./

# Ensure Firebase CLI is installed by running a version check
RUN firebase --version

# Expose necessary ports for Firebase Emulator
EXPOSE 8085 9099 9000 4000

# Default command for running Firebase Emulator
CMD ["firebase", "emulators:start", "--only", "database,firestore,auth"]