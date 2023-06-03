import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2


class Diagram:
    def __init__(self):
        self.values_list = [1] * 7
        self.categories_list = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        self.colors = ['red', 'green', 'blue', 'orange', 'purple', 'yellow', 'gray']

    def create_radar_chart(self, value):
        index = self.categories_list.index(value)
        self.values_list[index] += 1

        # Normalize the values to a scale of 0 to 100
        total = sum(self.values_list)
        normalized_values = [value * 100 / total for value in self.values_list]

        # Set up the plot with grey background and plot area
        fig = plt.figure(figsize=(4, 4), facecolor='#DCDCDC')
        ax = fig.add_subplot(111, polar=True, facecolor='#DCDCDC')

        # Remove unnecessary spines and gridlines
        ax.spines['polar'].set_visible(False)
        ax.grid(False)

        # Plot the data and connect first and last dots with a closed polygon
        angles = np.linspace(0, 2 * np.pi, len(self.categories_list), endpoint=False).tolist()
        normalized_values += normalized_values[:1]  # Close the polygon
        angles += angles[:1]  # Close the polygon
        ax.plot(angles, normalized_values, color='red', linewidth=2, linestyle='solid')
        ax.fill(angles, normalized_values, alpha=0.3, color='red')

        # Set the category labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(self.categories_list, color='black', fontsize=16, fontweight= 'bold')
        ax.set_yticklabels([])  # Hide radial axis labels
        ax.tick_params(axis='x', pad=8)  # Increase spacing between labels and plot

        # # Add data values as text annotations
        # for angle, value, category, color in zip(angles, normalized_values[:-1], self.categories_list, self.colors):
        #     ax.text(angle, value + 5, f'{value:.1f}', ha='center', va='center', color=color, fontsize=8)

        # Set the radial axis limits
        ax.set_ylim(0, 100)
        ax.set_yticks(np.linspace(0, 50, 6))
        ax.set_yticklabels([str(i) for i in range(0, 51, 10)], color='black')  # Set the tick label color to black
        ax.set_yticklabels([])  # Hide radial axis labels

        # Remove unnecessary spines and gridlines
        ax.spines['polar'].set_visible(False)
        ax.grid(False)

        plt.tight_layout()  # Adjust plot spacing


        # Convert the plot to an image
        fig.canvas.draw()
        diagram_image = np.array(fig.canvas.renderer.buffer_rgba())
        diagram_image = Image.fromarray(diagram_image)
        diagram_image = cv2.cvtColor(np.array(diagram_image), cv2.COLOR_RGBA2BGR)

        return diagram_image
