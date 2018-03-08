#include <stdafx.h>

// OpenGL
#include <GL/glew.h>
#include <GL/gl.h>
#include <GL/glu.h>

// glm
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

// freeglut
#include <GLFW/glfw3.h>

// stl
#include <vector>
#include <stdexcept>
#include <chrono>
#include <memory>

// Own
#include <OpenGL_Matrix_Camera.h>
#include <OpenGL_SimpleShaderProgram.h>


std::string sh_vert = R"(
#version 400

layout (location = 0) in vec3 inPos;
layout (location = 1) in vec4 inColor;

out vec3 vertPos;
out vec4 vertCol;

void main()
{
    vertCol     = inColor;
		vertPos     = inPos;
		gl_Position = vec4(inPos, 1.0);
}
)";

std::string sh_frag = R"(
#version 400

in vec3 vertPos;
in vec4 vertCol;

out vec4 fragColor;

void main()
{
    fragColor = vertCol;
}
)";


std::chrono::high_resolution_clock start_time;

std::unique_ptr<OpenGL::ShaderProgram> g_prog;


bool valid_viewport = false;

void Resize( GLFWwindow *, int , int );

int main(int argc, char** argv)
{
    if ( glfwInit() == 0 )
        throw std::runtime_error( "error initializing glfw" );

    GLFWwindow *wnd = glfwCreateWindow( 800, 600, "OGL window", nullptr, nullptr );
    if ( wnd == nullptr )
    {
        glfwTerminate();
        throw std::runtime_error( "error initializing window" ); 
    }
    glfwSetWindowSizeCallback( wnd, Resize );

    glfwMakeContextCurrent(wnd);

    if ( glewInit() != GLEW_OK )
        throw std::runtime_error( "error initializing glew" );

    g_prog.reset( new OpenGL::ShaderProgram(
    {
      { sh_vert, GL_VERTEX_SHADER },
      { sh_frag, GL_FRAGMENT_SHADER }
    } ) );

    static const std::vector<float> varray
    { 
      -0.707f, -0.75f,    1.0f, 0.0f, 0.0f, 1.0f, 
       0.707f, -0.75f,    1.0f, 1.0f, 0.0f, 1.0f,
       0.0f,    0.75f,    0.0f, 0.0f, 1.0f, 1.0f
    };

    GLuint vbo;
    glGenBuffers( 1, &vbo );
    glBindBuffer( GL_ARRAY_BUFFER, vbo );
    glBufferData( GL_ARRAY_BUFFER, varray.size()*sizeof(*varray.data()), varray.data(), GL_STATIC_DRAW );

    GLuint vao;
    glGenVertexArrays( 1, &vao );
    glBindVertexArray( vao );
    glVertexAttribPointer( 0, 2, GL_FLOAT, GL_FALSE, 6*sizeof(*varray.data()), 0 );
    glEnableVertexAttribArray( 0 );
    glVertexAttribPointer( 1, 4, GL_FLOAT, GL_FALSE, 6*sizeof(*varray.data()), (void*)(2*sizeof(*varray.data())) );
    glEnableVertexAttribArray( 1 );
    glBindBuffer( GL_ARRAY_BUFFER, 0 );

    g_prog->Use();

    //start_time = std::chrono::high_resolution_clock::now();
    
    while (!glfwWindowShouldClose(wnd))
    {
        if ( valid_viewport == false )
        {
          int vpSize[2];
          glfwGetFramebufferSize( wnd, &vpSize[0], &vpSize[1] );
          glViewport( 0, 0, vpSize[0], vpSize[1] );
          valid_viewport = true;
        }

        glClearColor(0.0f, 0.0f, 0.0f, 0.0f);  
        glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT);
      
        glDrawArrays( GL_TRIANGLES, 0, 3 );

        glfwSwapBuffers(wnd);
        glfwPollEvents();
    }

    g_prog.reset( nullptr );
    glfwDestroyWindow( wnd );
    wnd = nullptr;
    glfwTerminate();

    return 0;
}

void Resize( GLFWwindow *wnd, int cx, int cy )
{
  valid_viewport = false;
  // ....
}
