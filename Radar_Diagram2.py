import numpy as np
import matplotlib.pyplot as plt




class Diagram:
    def __init__(self):
        self.values_list = [1] * 7
        self.categories_list = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

    def create_radar_chart(self, value):
        index = self.categories_list.index(value)
        self.values_list[index] += 1

        # Normalize the values to a scale of 0 to 100
        normalized_values = [value * 100 / sum(self.values_list) for value in self.values_list]

        # Set up the plot with transparent background and plot area
        fig = plt.figure(figsize=(8, 8), facecolor='none')
        ax = fig.add_subplot(111, polar=True, facecolor='none')
        ax.patch.set_alpha(0)  # Set the background to be transparent

        # Plot the data and connect first and last dots, and set the line color to red
        ax.plot(np.linspace(0, 2 * np.pi, len(self.categories_list), endpoint=False), normalized_values, color='red')
        ax.plot(np.linspace(0, 2 * np.pi, len(self.categories_list) + 1, endpoint=True),
                normalized_values + [normalized_values[0]], color='red')

        # Fill in the area under the curve with a transparent color
        ax.fill(np.linspace(0, 2 * np.pi, len(self.categories_list), endpoint=False), normalized_values, alpha=0.3,
                color='red')

        # Set the category labels
        ax.set_xticks(np.linspace(0, 2 * np.pi, len(self.categories_list), endpoint=False))
        ax.set_xticklabels(self.categories_list, color='black')  # Set the label color to black

        # Remove the y-axis tick labels
        ax.set_yticklabels([])

        fig.canvas.draw()
        diagram_image = np.array(fig.canvas.renderer.buffer_rgba())

        # Convert the Matplotlib figure to a NumPy array

        # Display the plot
        return diagram_image










