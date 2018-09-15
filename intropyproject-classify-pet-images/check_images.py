#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# */AIPND-revision/intropyproject-classify-pet-images/check_images.py
#
# PROGRAMMER: Gareth Dwyer
# DATE CREATED: 14 September 2018
# REVISED DATE:
# PURPOSE: Classifies pet images using a pretrained CNN model, compares these
#          classifications to the true identity of the pets in the images, and
#          summarizes how well the CNN performed on the image classification task.
#          Note that the true identity of the pet (or object) in the image is
#          indicated by the filename of the image. Therefore, your program must
#          first extract the pet image label from the filename before
#          classifying the images using the pretrained CNN model. With this
#          program we will be comparing the performance of 3 different CNN model
#          architectures to determine which provides the 'best' classification.
#
# Use argparse Expected Call with <> indicating expected user input:
#      python check_images.py --dir <directory with images> --arch <model>
#             --dogfile <file that contains dognames>
#   Example call:
#    python check_images_solution.py --dir pet_images/ --arch vgg --dogfile dognames.txt
##

from time import time, sleep

from print_functions_for_lab_checks import *

from get_input_args import get_input_args
from get_pet_labels import get_pet_labels
from classify_images import classify_images
from adjust_results4_isadog import adjust_results4_isadog
from calculates_results_stats import calculates_results_stats
from print_results import print_results

def main():
    # start the timer and parse any args from the user
    start_time = time()
    in_arg = get_input_args()
    check_command_line_arguments(in_arg)

    # infer the correct answers from the image file names
    results = get_pet_labels(in_arg.dir)
    check_creating_pet_image_labels(results)

    # predict the result for each image, for the given architecture
    classify_images(in_arg.dir, results, in_arg.arch)
    check_classifying_images(results)

    # aggregate the results to dog not-dog level
    adjust_results4_isadog(results, in_arg.dogfile)
    check_classifying_labels_as_dogs(results)

    # calculate accuracy and some other aggregate statistics
    results_stats = calculates_results_stats(results)
    check_calculating_results(results, results_stats)

    # print the final results for this architecture and stop the timer
    print_results(results, results_stats, in_arg.arch, True, True)
    end_time = time()

    tot_time = (end_time - start_time)
    print("\n** Total Elapsed Runtime:",
          str(int((tot_time/3600)))+":"+str(int((tot_time%3600)/60))+":"
          +str(int((tot_time%3600)%60)) )

    import pickle
    with open("results_stats.pickle", "wb") as f:
        pickle.dump(results_stats, f)
    print()
    print()
    print("****** FINAL RESULTS *******")
    print()
    print()
    print("{}       {}          {}       {}       {}".format("Architecture", "~Dog", "Dog", "Breed", "Label"))

    print("{}{}{:.2f}       {:.2f}     {:.2f}       {:.2f}".format(in_arg.arch, " " * (19 - len(in_arg.arch)), results_stats['pct_correct_notdogs'], results_stats['pct_correct_dogs'], results_stats['pct_correct_breed'], results_stats['pct_match']))

    print()
    print()
    print("*******************************")


# Call to main function to run the program
if __name__ == "__main__":
    main()
