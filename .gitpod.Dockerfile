FROM gitpod/workspace-full:2023-05-08-21-16-55

# Some datasets work on 3.8 only
RUN pyenv install 3.8.15\
    && pyenv global 3.8.15